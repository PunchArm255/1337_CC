#!/usr/bin/env python3
"""Exercise 01: handling different built-in error types."""


def garden_operations(test: str) -> None:
    """Trigger a specific error type based on the test argument.

    Args:
        test: Error type key ("value", "zero", "file", or "key").
    """
    if test == "value":
        int("abc")
    elif test == "zero":
        print(1 // 0)
    elif test == "file":
        open("missing.txt", "r")
    elif test == "key":
        d = {}
        print(d["missing_plant"])


def test_error_types() -> None:
    """Run demonstrations of catching different error types."""
    print("=== Garden Error Types Demo ===\n")

    print("Testing ValueError...")
    try:
        garden_operations("value")
    except ValueError as e:
        print(f"Caught ValueError: {e}\n")

    print("Testing ZeroDivisionError...")
    try:
        garden_operations("zero")
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}\n")

    print("Testing FileNotFoundError...")
    try:
        garden_operations("file")
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}\n")

    print("Testing KeyError...")
    try:
        garden_operations("key")
    except KeyError as e:
        print(f"Caught KeyError: {e}\n")

    print("Testing multiple errors together...")
    try:
        garden_operations("value")
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught an error, but program continues!\n")

    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
