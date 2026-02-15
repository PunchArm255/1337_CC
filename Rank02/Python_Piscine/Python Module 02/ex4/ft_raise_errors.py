#!/usr/bin/env python3
"""Exercise 04: raising errors with custom validation logic."""

from typing import Optional


def check_plant_health(
    plant_name: Optional[str],
    water_level: int,
    sunlight_hours: int,
) -> Optional[str]:
    """Validate plant health parameters and raise on invalid input.

    Args:
        plant_name: Name of the plant to check (can be None).
        water_level: Water level between 1 and 10.
        sunlight_hours: Sunlight hours between 2 and 12.

    Returns:
        A health status message if all checks pass, None otherwise.

    Raises:
        ValueError: If any parameter is out of the valid range.
    """
    if plant_name == "" or plant_name is None:
        raise ValueError("Error: Plant name cannot be empty!\n")
    elif water_level < 1:
        raise ValueError(f"Error: Water level {water_level} "
                         "is too low (min 1)\n")
    elif water_level > 10:
        raise ValueError(f"Error: Water level {water_level} "
                         "is too high (max 10)\n")
    elif sunlight_hours < 2:
        raise ValueError(f"Error: Sunlight hours {sunlight_hours} "
                         "are too low (min 2)\n")
    elif sunlight_hours > 12:
        raise ValueError(f"Error: Sunlight hours {sunlight_hours} "
                         "are too high (max 12)\n")
    else:
        msg = f"Plant '{plant_name}' is healthy!\n"
        print(msg)
        return msg
    return None


def test_plant_checks() -> None:
    """Test plant health checks with valid and invalid inputs."""
    print("=== Garden Plant Health Checker ===\n")

    print("Testing good values...")
    check_plant_health("tomato", 10, 10)

    print("Testing empty plant name...")
    try:
        check_plant_health("", 10, 10)
    except ValueError as e:
        print(e)

    print("Testing bad water level...")
    try:
        check_plant_health("tomato", 15, 10)
    except ValueError as e:
        print(e)

    print("Testing bad sunlight hours...")
    try:
        check_plant_health("tomato", 10, 0)
    except ValueError as e:
        print(e)

    print("All error raising tests completed!")


if __name__ == "__main__":
    test_plant_checks()
