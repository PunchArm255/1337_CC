#!/usr/bin/env python3

def garden_operations(test):
    if test == "value":
        print("Testing ValueError...")
        int("abc")
    elif test == "zero":
        print("Testing ZeroDivisionError...")
        print(1 / 0)
    elif test == "file":
        print("Testing FileNotFoundError...")
        open("missing.txt", "r")
    elif test == "key":
        print("Testing KeyError...")
        d = {}
        print(d["missing_plant"])

def test_error_types():
    print("=== Garden Error Types Demo ===")
    
    try:
        garden_operations("value")
    except ValueError as e:
        print(f"Caught ValueError: {e}")

    try:
        garden_operations("zero")
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}")

    try:
        garden_operations("file")
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}")

    try:
        garden_operations("key")
    except KeyError as e:
        print(f"Caught KeyError: {e}")

    print("Testing multiple errors together...")
    try:
        garden_operations("zero")
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught an error, but program continues!")

    print("All error types tested successfully!")

if __name__ == "__main__":
    test_error_types()