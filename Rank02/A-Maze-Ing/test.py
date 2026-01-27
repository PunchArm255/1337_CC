#!/usr/bin/env python

from typing import Dict
import sys 
import random


def first_args_validation() -> Dict:
    """This is the first step validation, which is to check for file opening
    operation, and syntax error validation
    Return a Dict of all valid configurations for the next step validation,
    or exit the program if there's errors.
    """
    config_variables = []
    valid_configs = []
    errors = []

    if len(sys.argv) < 2:
        print("Error: No configuration provided."
              "\nUsage: python3 a_maze_ing.py <config.txt>")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("Warning: Too many arguments provided."
              "Only the first one will be used\n")

    # File-level errors handling:
    # File not found, Cannot open file, No read permission
    config_file = sys.argv[1]
    try:
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                config_variables.append(line)
    except FileNotFoundError:
        print(f"[Error]: Cannot open file '{config_file}'\n"
              "Error detail: File not found")
        sys.exit(1)
    except PermissionError:
        print(f"[Error]: Cannot open file '{config_file}'\n"
              "Error detail: Permission error")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    # Second-level errors handling:
    # Syntax error (formatting):
    for config in config_variables:
        # check for Wrong format (= instead of :)
        if '=' not in config and ':' in config:
            errors.append("Wrong configuration format: ':' "
                          f"is used instead of '=' in {config}")
            continue

        # check for extra "=" symbol
        if config.count('=') != 1:
            errors.append("Bad configuration syntax: "
                          f"use of multiple '=' in {config}")
            continue

        key, value = config.split('=')

        # check for missing key or missing value
        if not key:
            errors.append("Bad configuration syntax: "
                          f"missing key in: {config}")
            continue
        if not value:
            errors.append("Bad configuration syntax: "
                          f"missing value in: {config}")
            continue

        # take if valid
        valid_configs.append((key, value))

    # Check if there's any error, print them and exit the program
    if errors:
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    # return if all configs are valid
    return dict(valid_configs)


def semantic_validation(config_values: Dict) -> Dict:
    """
    Check for all required keys, parsable value
    """
    typed_configs = {}
    errors = []

    # check missing keys
    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT"]
    missing_keys = [k for k in required_keys if k not in config_values]

    if missing_keys:
        print("Semantic error found:")
        for err in missing_keys:
            print(f"Missing required key: '{err}'")
        sys.exit(1)

    # validate WIDTH & HEIGHT convert to int and must be > 0
    for key in ("WIDTH", "HEIGHT"):
        try:
            num = int(config_values[key])
            if num <= 0:
                errors.append(f"{key} must be > 0")
            typed_configs[key] = num
        except ValueError:
            errors.append(f"{key} must be integer, got '{config_values[key]}' instead")

    if errors:
        print("Semantic error found:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    width, height = typed_configs["WIDTH"], typed_configs["HEIGHT"]

    # Parse ENTRY & EXIT
    

if __name__ == "__main__":
    configs = first_args_validation()
    x = semantic_validation(configs)
    print("yes, shit works 🗣️\n")
    print(x)