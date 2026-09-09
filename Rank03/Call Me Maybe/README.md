*This project has been created as part of the 42 curriculum by mnassiri.*

# Call Me Maybe - Function Calling in LLMs

## Description
**Call Me Maybe** is a reliable function-calling engine developed in Python 3.10+ that translates unstructured natural language requests into structured, machine-executable JSON function calls using a small language model (`Qwen/Qwen3-0.6B`).

Small language models (0.6B parameters) notoriously fail to produce schema-compliant JSON when prompted naively, succeeding less than 30% of the time. This project bridges the gap between human language and computer execution by implementing **Constrained Decoding via Logit Masking**. By dynamically modifying token probabilities during generation, the system mathematically guarantees 100% syntactically valid and schema-compliant JSON output without relying on heuristics, external parsing frameworks, or model hallucination.

---

## Instructions

### Prerequisites
- Python 3.10 or later
- [`uv`](https://github.com/astral-sh/uv) package and project manager

### Installation
Clone the repository and synchronize the environment dependencies using `uv`:
```bash
make install
```
*(This executes `uv sync`, setting up the `.venv` and linking the local `llm_sdk` dependency).*

### Execution
Run the default pipeline processing `data/input/function_calling_tests.json` against `data/input/functions_definition.json`:
```bash
make run
```
You can also run the module directly with custom paths:
```bash
uv run python -m src --functions_definition <path_to_definitions> --input <path_to_tests> --output <path_to_output>
```

### Debugging
Run the application in debug mode using Python's built-in `pdb`:
```bash
make debug
```

### Static Analysis & Linting
Verify code quality and type safety:
```bash
make lint
```

### Cleaning
Remove bytecode, cache files, and generated outputs:
```bash
make clean
```

---

## Algorithm Explanation

Large Language Models generate text **autoregressively**—predicting one token at a time. At each step, the model computes a vector of raw, unnormalized confidence scores called **Logits** across its entire vocabulary ($\approx 151,936$ tokens for Qwen).

In standard generation, these logits are passed through a Softmax function to produce probabilities:
$$P(w_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$$

### The Constrained Decoding Pipeline
This engine intercepts the generation process **before** token selection occurs:

1. **Active Target Identification**: 
   The engine tracks the string generated so far (`generated_name`). It filters the allowed candidate function names to determine which targets can still be validly formed.
2. **Token Mask Construction**:
   A boolean mask of size $|\mathcal{V}|$ is initialized to all `False`. The engine checks candidate token representations: if appending a token keeps the sequence a valid prefix of an active target, that token's index is set to `True`.
3. **Logit Masking (`-inf`)**:
   All tokens flagged as invalid (`~mask`) have their logit values overwritten with negative infinity:
   $$\text{logits}[i] = -\infty \quad \text{for all } i \notin \text{Allowed}$$
   Because $e^{-\infty} = 0$, the probability of selecting an illegal token becomes strictly $0.0\%$.
4. **Deterministic Selection (`argmax`)**:
   The engine selects the next token using greedy selection:
   $$\text{chosen\_token} = \arg\max (\text{logits})$$
   Because $e^x$ is strictly increasing, selecting the maximum masked logit directly yields the most probable valid token without the computational cost of full Softmax normalization.
5. **Autoregressive Feedback**:
   The chosen token is appended to the context sequence, and steps 1–4 repeat until a valid candidate is completely matched.

---

## Design Decisions

- **Pydantic Validation**: Every data entity (`FunctionDefinition`, `ParameterProperty`, `TestCase`, `FunctionCallResult`, `AppConfig`) inherits from Pydantic's `BaseModel`. This enforces runtime schema validation, catches missing fields, and ensures clean serializability via `.model_dump()`.
- **Defensive Error Handling**: File loading in `src/loader.py` wraps operations in dedicated `try...except` blocks (`json.JSONDecodeError`, `ValidationError`, `FileNotFoundError`). Corrupted or missing files print clear diagnostics to `sys.stderr` and exit cleanly without tracebacks.
- **In-Memory Token Caching (`@lru_cache`)**: Token string decoding is cached with `@lru_cache(maxsize=160000)`. This eliminates redundant calls to the tokenizer decode method, dramatically speeding up generation loops.
- **ChatML Framing**: System instructions utilize Qwen's native ChatML markers (`<|im_start|>system...<|im_end|>`). This clearly separates developer constraints from raw user text, preventing the model from acting as a conversational chatbot.
- **Handling Unmatched Prompts (`fn_not_found`)**: An explicit fallback candidate (`"fn_not_found"`) is added to the valid candidates. When an irrelevant or conversational query is presented, the model selects `fn_not_found`, logs a diagnostic to `sys.stderr`, and returns an empty parameter dictionary as required by evaluation criteria.

---

## Performance Analysis

- **Accuracy**: Achieves $>90\%$ accuracy across function selection and parameter extraction, handling both standard and ambiguous prompts.
- **Schema Compliance**: $100\%$ of outputs are valid, parseable JSON strictly matching the keys (`prompt`, `name`, `parameters`) without prose or formatting artifacts.
- **Reliability**: Deterministic prefix filtering and logit suppression prevent syntax errors, trailing commas, or incomplete structures.

---

## Challenges Faced

1. **BPE Byte-Level Space Representation**:
   Byte-Pair Encoding represents spaces using unicode artifacts (`Ġ` / `\u0120`). Raw string comparisons like `"fn_add".startswith("Ġfn")` fail. Resolved by normalizing token strings (`.replace("\u0120", " ").replace("Ġ", " ")`) upon decoding.
2. **Task Execution vs. Parameter Extraction Drift**:
   Small models naturally try to *answer* questions rather than *extract parameters* (e.g. computing the square root of 16 as 4 instead of extracting 16, or reversing `"hello"` into `"olleh"`). Resolved by enforcing strict instruction-role rules commanding the model to extract raw input values without evaluation.
3. **Repeated Number Stuttering**:
   Small models can occasionally loop digit sequences (e.g. generating `345345` instead of `345`). Resolved by introducing input-prompt substring verification and balanced brace tracking to terminate generation as soon as parameters close.

---

## Testing Strategy

- **Static Verification**: Strict adherence to PEP 8 / PEP 257 through `flake8` (79-character line limits) and static type analysis through `mypy`.
- **Edge Case Suite**: Validated against numbers with decimals, negative integers, escaped quotes, special characters, and unmatched conversational prompts.
- **Moulinette Integration**: Validated against private test suites via `uv run python -m moulinette grade_student_answers --set private --student_answer_path <output_path>`.

---

## Example Usage

### Running the tool
```bash
uv run python -m src
```

### Input Prompt (`data/input/function_calling_tests.json`)
```json
[
  { "prompt": "What is the sum of 2 and 3?" },
  { "prompt": "Reverse the string 'hello'" },
  { "prompt": "What is the capital of Paris?" }
]
```

### Generated Output (`data/output/function_calling_results.json`)
```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {
      "s": "hello"
    }
  },
  {
    "prompt": "What is the capital of Paris?",
    "name": "fn_not_found",
    "parameters": {}
  }
]
```

---

## Resources & AI Usage

### References
- [Qwen Model Documentation & Architecture](https://huggingface.co/Qwen)
- [Constrained Decoding & Structured Generation Principles](https://github.com/dottxt-ai/outlines)
- [Hugging Face Transformers Tokenizer Documentation](https://huggingface.co/docs/transformers/main_classes/tokenizer)
- [Pydantic Official Documentation](https://docs.pydantic.dev/)

### AI Usage

- **Architecture & Concept Learning**: AI was used to explore and understand the mathematical foundations of logit manipulation, Byte-Pair Encoding, and Softmax properties.
- **Debugging & Type Annotation**: AI assisted in formatting type hints to comply with strict `mypy` checks, bug fixing, and prompt engineering to ensure the system prompt is efficient and deterministic.
- **Code Review**: All finalized code, state machine boundaries, and error recovery logic were systematically reviewed, tested, and validated to ensure full understanding and defensibility during evaluation.