#!/usr/bin/env python3
"""Exercise 00: first exception handling with try/except."""

from typing import Optional


def check_temperature(temp_str: str) -> Optional[int]:
    """Check if temperature string is valid and within plant range.

    Args:
        temp_str: A string representing the temperature value.

    Returns:
        The temperature as int if valid and in range, None otherwise.
    """
    try:
        temp = int(temp_str)
        if 0 <= temp <= 40:
            print(f"Temperature {temp}°C is perfect for plants!\n")
            return temp
        elif temp < 0:
            print(f"Error: {temp}°C is too cold for plants (min 0°C)\n")
        else:
            print(f"Error: {temp}°C is too hot for plants (max 40°C)\n")

    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number\n")
    return None


def test_temperature_input() -> None:
    """Test temperature checking with various valid and invalid inputs."""
    print("=== Garden Temperature Checker ===\n")

    print("Testing temperature: 25")
    check_temperature("25")

    print("Testing temperature: abc")
    check_temperature("abc")

    print("Testing temperature: 100")
    check_temperature("100")

    print("Testing temperature: -50")
    check_temperature("-50")

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature_input()
