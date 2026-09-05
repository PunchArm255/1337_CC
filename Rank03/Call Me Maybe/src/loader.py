"""File loader utility with error handling and Pydantic validation."""

import json
import os
import sys
from pydantic import ValidationError

from src.models import FunctionDefinition, TestCase


def load_functions_definition(path: str) -> list[FunctionDefinition]:
    """Load and validate available function definitions from a JSON file.

    Args:
        path: File system path to the functions definition JSON file.

    Returns:
        List of validated FunctionDefinition models.
    """
    if not os.path.exists(path):
        print(f"Error: Functions definition file not found: {path}",
              file=sys.stderr)
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        if not isinstance(raw_data, list):
            print(f"Error: Expected a JSON array in {path}", file=sys.stderr)
            return []

        return [FunctionDefinition.model_validate(item) for item in raw_data]

    except json.JSONDecodeError as err:
        print(f"Error: Invalid JSON format in {path}: {err}", file=sys.stderr)
        return []
    except ValidationError as err:
        print(f"Error: Schema validation failed for {path}: {err}",
              file=sys.stderr)
        return []
    except Exception as err:
        print(f"Error reading {path}: {err}", file=sys.stderr)
        return []


def load_test_cases(path: str) -> list[TestCase]:
    """Load and validate test prompt items from a JSON file.

    Args:
        path: File system path to the input tests JSON file.

    Returns:
        List of validated TestCase models.
    """
    if not os.path.exists(path):
        print(f"Error: Input tests file not found: {path}", file=sys.stderr)
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        if not isinstance(raw_data, list):
            print(f"Error: Expected a JSON array in {path}", file=sys.stderr)
            return []

        return [TestCase.model_validate(item) for item in raw_data]

    except json.JSONDecodeError as err:
        print(f"Error: Invalid JSON format in {path}: {err}", file=sys.stderr)
        return []
    except ValidationError as err:
        print(f"Error: Schema validation failed for {path}: {err}",
              file=sys.stderr)
        return []
    except Exception as err:
        print(f"Error reading {path}: {err}", file=sys.stderr)
        return []