#!/usr/bin/env python3
"""Exercise 02: creating and using custom exception classes."""


class GardenError(Exception):
    """Base exception for all garden-related errors."""

    pass


class PlantError(GardenError):
    """Exception raised for plant-related issues."""

    pass


class WaterError(GardenError):
    """Exception raised for water-related issues."""

    pass


def test_custom_errors() -> None:
    """Demonstrate raising and catching custom exception classes."""
    print("=== Custom Garden Errors Demo ===\n")

    print("Testing PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!\n")
    except PlantError as e:
        print(f"Caught PlantError: {e}")

    print("Testing WaterError...")
    try:
        raise WaterError("Not enough water in the tank!\n")
    except WaterError as e:
        print(f"Caught WaterError: {e}")

    print("Testing catching all garden errors...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except GardenError as e:
        print(f"Caught a garden error: {e}")

    try:
        raise WaterError("Not enough water in the tank!\n")
    except GardenError as e:
        print(f"Caught a garden error: {e}")

    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
