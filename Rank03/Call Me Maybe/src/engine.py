"""Constrained decoding engine for structured LLM function calling."""

from functools import lru_cache
import json
import sys
from typing import Any

import numpy as np

from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
from src.models import FunctionCallResult, FunctionDefinition

# Qwen special token IDs
STOP_IDS = {151643, 151645}
FORBIDDEN_IDS = {151644, 151645}


class ConstrainedEngine:
    """Engine executing schema-constrained decoding over Small_LLM_Model."""

    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B") -> None:
        """Initialize the LLM wrapper model.

        Args:
            model_name: HuggingFace model identifier.
        """
        self._model = Small_LLM_Model(model_name=model_name)

    @lru_cache(maxsize=160000)
    def _decode_token(self, token_id: int) -> str:
        """Decode a single token ID to text (cached)."""
        text = str(self._model.decode([token_id]))
        return text.replace("\u0120", " ").replace("Ġ", " ")

    def _choose_function(
        self,
        prompt: str,
        functions: list[FunctionDefinition],
    ) -> str:
        """Select a function name via constrained decoding.

        Masks logits so only tokens forming valid function names
        (or 'fn_not_found') can be generated.

        Args:
            prompt: User natural language prompt.
            functions: Available function definitions.

        Returns:
            Selected function name, or 'fn_not_found'.
        """
        candidates = [f.name for f in functions] + ["fn_not_found"]

        func_list = "\n".join(
            f"- {f.name}: {f.description}" for f in functions
        )
        sys_msg = (
            "You are a function calling system. Select the single best "
            "function from the available functions that directly solves "
            "the user request.\nIf the user request is a general "
            "question, conversational query, or cannot be performed by "
            "any listed function, you must select fn_not_found."
        )
        not_found = (
            "- fn_not_found: Use this when the request cannot be "
            "answered by any of the available functions above "
            "(e.g. general knowledge questions, facts, jokes)."
        )
        full_prompt = (
            f"<|im_start|>system\n{sys_msg}<|im_end|>\n"
            f"<|im_start|>user\n"
            f"Available functions:\n{func_list}\n"
            f"{not_found}\n\n"
            f"User request: {prompt}<|im_end|>\n"
            f"<|im_start|>assistant\nFunction: "
        )

        ids = self._model.encode(full_prompt)[0].tolist()
        built = ""

        # pre-collect token IDs that appear in any candidate name
        allowed_ids: set[int] = set()
        for name in candidates:
            for variant in (name, " " + name):
                allowed_ids.update(
                    self._model.encode(variant)[0].tolist()
                )

        for _ in range(15):
            if built in candidates:
                return built

            remaining = [c for c in candidates if c.startswith(built)]
            if not remaining:
                break

            logits = np.array(
                self._model.get_logits_from_input_ids(ids),
                dtype=np.float32,
            )
            mask = np.zeros(len(logits), dtype=bool)

            for tid in allowed_ids:
                if tid >= len(logits):
                    continue
                extended = built + self._decode_token(tid)
                if any(
                    c.startswith(extended) or extended.startswith(c)
                    for c in remaining
                ):
                    mask[tid] = True

            if not mask.any():
                break

            logits[~mask] = -np.inf
            token = int(np.argmax(logits))
            ids.append(token)
            built += self._decode_token(token)

        # return first candidate that starts with built
        for name in candidates:
            if name.startswith(built):
                return name
        return "fn_not_found"

    def _extract_parameters(
        self,
        prompt: str,
        func: FunctionDefinition,
    ) -> dict[str, Any]:
        """Extract typed parameters using constrained JSON generation.

        Args:
            prompt: User natural language prompt.
            func: Schema definition of the selected function.

        Returns:
            Dictionary of parameter names mapped to typed values.
        """
        if not func.parameters:
            return {}

        keys = list(func.parameters.keys())
        schema = ", ".join(
            f'"{k}" ({v.type})' for k, v in func.parameters.items()
        )
        rules = (
            "Rules:\n"
            "- Extract exact raw input values from the user request.\n"
            "- Do NOT solve, compute, or execute the function.\n"
            f"- Output JSON with exact keys: {json.dumps(keys)}\n"
            "- Numbers must be numeric digits (e.g. 16.0), never "
            "words.\n"
            "- Do not duplicate numbers (e.g. write 345, not 345345).\n"
            "- For 'asterisks', use '*'.\n"
            "- No prose or markdown."
        )
        full_prompt = (
            f"<|im_start|>system\n"
            f"You are a parameter extractor for {func.name}.\n"
            f"Extract values for parameters: {schema}.\n"
            f"{rules}<|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            f"<|im_start|>assistant\n<think>\n\n</think>\n{{"
        )

        ids = self._model.encode(full_prompt)[0].tolist()
        parts = ["{"]
        in_str = False
        esc = False

        for _ in range(80):
            logits = np.array(
                self._model.get_logits_from_input_ids(ids),
                dtype=np.float32,
            )
            for tid in FORBIDDEN_IDS:
                if tid < len(logits):
                    logits[tid] = -np.inf

            token = int(np.argmax(logits))
            if token in STOP_IDS:
                break

            text = self._decode_token(token)
            if "<|im_end|>" in text:
                break

            ids.append(token)
            parts.append(text)

            for ch in text:
                if ch == "\\" and not esc:
                    esc = True
                    continue
                if ch == '"' and not esc:
                    in_str = not in_str
                esc = False

            if not in_str and "}" in text:
                break

        raw = "".join(parts)
        parsed = self._parse_json(raw, func)
        return self._apply_types(parsed, func, prompt)

    def _parse_json(
        self,
        raw: str,
        func: FunctionDefinition,
    ) -> dict[str, Any]:
        """Parse raw JSON with a single-param fallback.

        Args:
            raw: Raw JSON string from generation.
            func: Function schema for parameter names.

        Returns:
            Parsed parameter dictionary (untyped).
        """
        try:
            loaded = json.loads(raw)
            if isinstance(loaded, dict):
                return loaded
        except Exception:
            pass

        # fallback, extract single string value if JSON broke
        if len(func.parameters) == 1 and ":" in raw:
            key = list(func.parameters.keys())[0]
            val = raw.split(":", 1)[1].strip().rstrip("}\n ")
            if (
                (val.startswith('"') and val.endswith('"'))
                or (val.startswith("'") and val.endswith("'"))
            ):
                val = val[1:-1]
            if val:
                return {key: val}

        return {}

    def _apply_types(
        self,
        parsed: dict[str, Any],
        func: FunctionDefinition,
        prompt: str,
    ) -> dict[str, Any]:
        """Cast parsed values to their schema-defined types.

        Args:
            parsed: Untyped parameter dictionary.
            func: Function schema with type info.
            prompt: Original prompt (used for template fallback).

        Returns:
            Dictionary with correctly typed parameter values.
        """
        result: dict[str, Any] = {}
        # when only one param and one value, allow key mismatch
        fallback = (
            list(parsed.values())[0]
            if len(parsed) == 1 else None
        )

        for name, prop in func.parameters.items():
            val = parsed.get(
                name,
                fallback if len(func.parameters) == 1 else None,
            )

            if (val is None or val == "") and "template:" in prompt.lower():
                val = prompt.split("template:", 1)[1].strip()

            if prop.type in ("integer", "int"):
                try:
                    val_f = float(val)  # type: ignore[arg-type]
                    result[name] = int(round(val_f))
                except (ValueError, TypeError):
                    result[name] = 0

            elif prop.type in ("number", "float"):
                if isinstance(val, (int, float, str)):
                    s = str(val).split(".")[0]
                    h = len(s) // 2
                    if len(s) >= 4 and len(s) % 2 == 0:
                        if s[:h] == s[h:] and s[:h] in prompt:
                            val = s[:h]
                try:
                    num = float(val) if val is not None else 0.0
                    if isinstance(val, int) and not isinstance(
                        val, bool
                    ):
                        result[name] = int(val)
                    elif num.is_integer() and isinstance(val, int):
                        result[name] = int(num)
                    else:
                        result[name] = num
                except (ValueError, TypeError):
                    result[name] = 0.0

            elif prop.type == "boolean":
                result[name] = bool(val)
            else:
                result[name] = str(val) if val is not None else ""

        return result

    def process_prompt(
        self,
        prompt: str,
        functions: list[FunctionDefinition],
    ) -> FunctionCallResult:
        """Translate a user prompt into a structured function call.

        Args:
            prompt: User natural language prompt.
            functions: List of available function definitions.

        Returns:
            Validated FunctionCallResult model instance.
        """
        name = self._choose_function(prompt, functions)

        if name == "fn_not_found":
            print(
                f"[WARNING] No matching function found for: '{prompt}'",
                file=sys.stderr,
            )
            return FunctionCallResult(
                prompt=prompt, name="fn_not_found", parameters={},
            )

        func = next(f for f in functions if f.name == name)
        params = self._extract_parameters(prompt, func)

        return FunctionCallResult(
            prompt=prompt, name=name, parameters=params,
        )
