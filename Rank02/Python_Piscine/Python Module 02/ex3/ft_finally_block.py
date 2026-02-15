#!/usr/bin/env python3
"""Exercise 03: using the finally block for cleanup."""

from typing import List, Optional


def water_plants(plant_list: List[Optional[str]]) -> None:
    """Water each plant in the list, with guaranteed cleanup.

    Args:
        plant_list: List of plant names (may contain None).
    """
    print("Opening watering system")
    try:
        for p in plant_list:
            if p is None:
                raise TypeError("Error: Cannot water None - invalid plant!")
            print(f"Watering {p}")

    except TypeError as e:
        print(e)

    finally:
        print("Closing watering system (cleanup)")


def test_watering_system() -> None:
    """Test the watering system with valid and invalid plant lists."""

    good_plants = ["tomato", "lettuce", "carrots"]
    bad_plants = ["tomato", None]

    print("=== Garden Watering System ===\n")

    print("Testing normal watering...")
    water_plants(good_plants)
    print("Watering completed successfully!\n")

    print("Testing with error...")
    water_plants(bad_plants)
    print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
