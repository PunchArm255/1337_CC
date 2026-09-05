"""Command line entrypoint for the function calling tool."""

import argparse
import json
import os
import sys

from src.loader import load_functions_definition, load_test_cases
from src.engine import ConstrainedEngine
from src.models import AppConfig, FunctionCallResult


def parse_arguments() -> AppConfig:
    """Parse and validate command line arguments.

    Returns:
        AppConfig populated with input and output paths.
    """
    parser = argparse.ArgumentParser(
        description="Call Me Maybe: LLM Function Calling Tool"
    )
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the JSON file with function definitions.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the JSON file with input prompts.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to save the generated function call results.",
    )

    args = parser.parse_args()
    return AppConfig(
        functions_path=args.functions_definition,
        input_path=args.input,
        output_path=args.output,
    )


def main() -> None:
    """Execute the batch function calling pipeline."""
    config = parse_arguments()

    # Gracefully validate and load input files
    functions = load_functions_definition(config.functions_path)
    if not functions:
        print("Error: No valid function definitions loaded. Aborting.",
              file=sys.stderr)
        sys.exit(1)

    test_cases = load_test_cases(config.input_path)
    if not test_cases:
        print("Error: No valid test prompts loaded. Aborting.",
              file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(functions)} functions and {len(test_cases)} tests.")
    print("Initializing Constrained Decoding Engine...")

    try:
        engine = ConstrainedEngine()
    except Exception as err:
        print(f"Error initializing LLM SDK: {err}", file=sys.stderr)
        sys.exit(1)

    results: list[FunctionCallResult] = []
    print("\n--- Generating Function Calls ---")
    for idx, test in enumerate(test_cases, 1):
        try:
            call_result = engine.process_prompt(test.prompt, functions)
            results.append(call_result)
            print(f"[{idx}/{len(test_cases)}] "
                  f"Prompt: '{test.prompt}' -> Call: {call_result.name}"
                  f"({call_result.parameters})")
        except Exception as err:
            print(f"Error processing prompt '{test.prompt}': {err}",
                  file=sys.stderr)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(config.output_path), exist_ok=True)

    try:
        output_data = [res.model_dump() for res in results]
        with open(config.output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nSuccess! Results written to {config.output_path}")
    except Exception as err:
        print(f"Error writing output file {config.output_path}: {err}",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
