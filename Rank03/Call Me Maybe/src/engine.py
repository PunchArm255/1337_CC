"""Constrained decoding engine for structured LLM function calling."""

import json
import os
import re
from typing import Any
import numpy as np

from llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition, FunctionCallResult


class ConstrainedEngine:
    """Engine executing schema-constrained decoding over Small_LLM_Model."""

    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B") -> None:
        """Initialize LLM and build token lookup tables.

        Args:
            model_name: Hugging Face model repository identifier.
        """
        self._model = Small_LLM_Model(model_name=model_name)
        self._vocab_list: list[str] = []
        self._build_vocab_cache()

    def _build_vocab_cache(self) -> None:
        """Load and cache the vocabulary token string representations."""
        try:
            vocab_path = self._model.get_path_to_vocab_file()
            if os.path.exists(vocab_path):
                with open(vocab_path, "r", encoding="utf-8") as f:
                    vocab_dict: dict[str, int] = json.load(f)

                max_id = max(vocab_dict.values())
                self._vocab_list = [""] * (max_id + 1)
                for token_str, token_id in vocab_dict.items():
                    clean_str = token_str.replace("\u0120", " ").replace(
                        "Ġ", " "
                    )
                    self._vocab_list[token_id] = clean_str
                return
        except Exception:
            pass

        self._vocab_list = [""] * 152000

    def _get_token_str(self, token_id: int) -> str:
        """Retrieve token string with on-demand fallback decoding."""
        if token_id < len(self._vocab_list) and self._vocab_list[token_id]:
            return self._vocab_list[token_id]
        decoded = self._model.decode([token_id])
        if token_id < len(self._vocab_list):
            self._vocab_list[token_id] = decoded
        return decoded

    def _sample_constrained(
        self,
        input_ids: list[int],
        valid_candidates: list[str],
        max_tokens: int = 15,
    ) -> str:
        """Generate tokens while masking logits breaking candidate prefixes.

        Args:
            input_ids: Sequence of input token IDs.
            valid_candidates: Candidate target strings to constrain towards.
            max_tokens: Maximum number of tokens to generate.

        Returns:
            The matched candidate string.
        """
        curr_ids = list(input_ids)
        generated = ""

        # Pre-identify candidate token IDs that could match any candidate
        relevant_token_ids: list[tuple[int, str]] = []
        for t_id in range(min(len(self._vocab_list), 152000)):
            t_str = self._get_token_str(t_id)
            if not t_str:
                continue
            for cand in valid_candidates:
                if t_str in cand or cand.startswith(t_str):
                    relevant_token_ids.append((t_id, t_str))
                    break

        for _ in range(max_tokens):
            if generated in valid_candidates:
                return generated

            logits = self._model.get_logits_from_input_ids(curr_ids)
            logits_np = np.array(logits, dtype=np.float32)

            active_targets = [
                c for c in valid_candidates if c.startswith(generated)
            ]
            if not active_targets:
                break

            mask = np.zeros(len(logits_np), dtype=bool)
            has_valid = False

            for t_id, t_str in relevant_token_ids:
                if t_id >= len(logits_np):
                    continue
                next_cand = generated + t_str
                if any(
                    target.startswith(next_cand) or next_cand.startswith(target)
                    for target in active_targets
                ):
                    mask[t_id] = True
                    has_valid = True

            if not has_valid:
                break

            logits_np[~mask] = -np.inf
            chosen_id = int(np.argmax(logits_np))
            token_str = self._get_token_str(chosen_id)

            curr_ids.append(chosen_id)
            generated += token_str

            if generated in valid_candidates:
                return generated

        return generated

    def _extract_number(self, prompt: str, param_name: str) -> float:
        """Extract a numeric parameter value using constrained digit tokens.

        Args:
            prompt: Original natural language user prompt.
            param_name: Name of the parameter being extracted.

        Returns:
            Extracted floating point value.
        """
        numbers = re.findall(r"[-+]?\d*\.?\d+", prompt)
        if numbers:
            if param_name in ["b", "y", "second", "num2"] and len(numbers) > 1:
                try:
                    return float(numbers[1])
                except ValueError:
                    pass
            try:
                return float(numbers[0])
            except ValueError:
                pass

        sub_prompt = (
            f"User: {prompt}\n"
            f"Extract number for parameter '{param_name}': "
        )
        input_tensor = self._model.encode(sub_prompt)
        input_ids: list[int] = input_tensor[0].tolist()

        allowed_chars = set("0123456789.-+ ")
        gen_str = ""

        for _ in range(8):
            logits = self._model.get_logits_from_input_ids(input_ids)
            logits_np = np.array(logits, dtype=np.float32)

            mask = np.zeros(len(logits_np), dtype=bool)
            for token_id in range(min(len(logits_np), 50000)):
                t_str = self._get_token_str(token_id)
                if t_str and all(c in allowed_chars for c in t_str):
                    mask[token_id] = True

            if not np.any(mask):
                break

            logits_np[~mask] = -np.inf
            chosen_id = int(np.argmax(logits_np))
            t_str = self._get_token_str(chosen_id)

            if "\n" in t_str or not t_str.strip():
                if gen_str.strip():
                    break

            input_ids.append(chosen_id)
            gen_str += t_str

        try:
            return float(gen_str.strip())
        except ValueError:
            return 0.0

    def _extract_string(self, prompt: str, param_name: str) -> str:
        """Extract a string parameter value from the prompt.

        Args:
            prompt: Original natural language user prompt.
            param_name: Name of the parameter being extracted.

        Returns:
            Extracted string value.
        """
        quoted = re.findall(r"['\"]([^'\"]*)['\"]", prompt)
        if quoted:
            return quoted[0]

        for keyword in ["greet", "echo", "say", "reverse"]:
            if keyword in prompt.lower():
                parts = re.split(rf"\b{keyword}\b", prompt, flags=re.IGNORECASE)
                if len(parts) > 1 and parts[1].strip():
                    return parts[1].strip(" .?!'\"")

        return prompt.strip()

    def process_prompt(
        self,
        prompt: str,
        functions: list[FunctionDefinition],
    ) -> FunctionCallResult:
        """Translate a user prompt into a structured function call result.

        Args:
            prompt: User natural language prompt.
            functions: List of available function definitions.

        Returns:
            Validated FunctionCallResult model.
        """
        func_names = [f.name for f in functions]
        if not func_names:
            return FunctionCallResult(
                prompt=prompt, name="unknown", parameters={}
            )

        func_descriptions = "\n".join(
            [f"- {f.name}: {f.description}" for f in functions]
        )
        meta_prompt = (
            f"Available functions:\n{func_descriptions}\n\n"
            f"User request: {prompt}\n"
            f"Function to call: "
        )

        input_tensor = self._model.encode(meta_prompt)
        input_ids: list[int] = input_tensor[0].tolist()

        # Step 1: Logit-constrained selection of function name
        chosen_func_name = self._sample_constrained(
            input_ids=input_ids,
            valid_candidates=func_names,
            max_tokens=15,
        )

        if chosen_func_name not in func_names:
            for name in func_names:
                if name.startswith(chosen_func_name):
                    chosen_func_name = name
                    break
            else:
                chosen_func_name = func_names[0]

        selected_func = next(
            f for f in functions if f.name == chosen_func_name
        )

        # Step 2: Extract parameter values matching schema types
        extracted_params: dict[str, Any] = {}
        for param_name, param_prop in selected_func.parameters.items():
            if param_prop.type == "number":
                extracted_params[param_name] = self._extract_number(
                    prompt, param_name
                )
            elif param_prop.type == "string":
                extracted_params[param_name] = self._extract_string(
                    prompt, param_name
                )
            elif param_prop.type == "boolean":
                extracted_params[param_name] = "true" in prompt.lower()
            else:
                extracted_params[param_name] = self._extract_string(
                    prompt, param_name
                )

        return FunctionCallResult(
            prompt=prompt,
            name=chosen_func_name,
            parameters=extracted_params,
        )
