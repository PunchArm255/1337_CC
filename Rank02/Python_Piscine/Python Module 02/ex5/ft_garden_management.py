#!/usr/bin/env python3
"""Exercise 05: full garden management system using exceptions."""

from typing import List, Optional


class GardenError(Exception):
    """Base exception for all garden-related errors."""

    pass


class PlantError(GardenError):
    """Exception raised for plant-related issues."""

    pass


class WaterError(GardenError):
    """Exception raised for water-related issues."""

    pass


class GardenManager:
    """Manage a garden with plants, watering, and health checks."""

    def __init__(self) -> None:
        """Initialize an empty garden manager."""
        self.plant_list: List[str] = []

    def add_plants(self, plant_name: Optional[str]) -> None:
        """Add a plant to the garden by name.

        Args:
            plant_name: Name of the plant to add (cannot be empty/None).
        """
        try:
            if plant_name == "" or plant_name is None:
                raise PlantError("Error adding plant: "
                                 "Plant name cannot be empty!")
            self.plant_list.append(plant_name)
            print(f"Added {plant_name} successfully")

        except PlantError as e:
            print(e)

    def water_plants(self) -> None:
        """Water all plants in the garden with guaranteed cleanup."""
        print("Opening watering system")
        try:
            for p in self.plant_list:
                if p == "" or p is None:
                    raise WaterError(
                        "Error: Watering failed - invalid plant!"
                    )
                print(f"Watering {p} - success")

        except WaterError as e:
            print(e)

        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(
        self,
        plant_name: Optional[str],
        water_level: int,
        sunlight_hours: int,
    ) -> None:
        """Validate plant health by checking water and sunlight levels.

        Args:
            plant_name: Name of the plant to check.
            water_level: Water level between 1 and 10.
            sunlight_hours: Sunlight hours between 2 and 12.
        """
        try:
            if plant_name == "" or plant_name is None:
                raise PlantError("Error: Plant name cannot be empty!")
            elif water_level < 1:
                raise WaterError(
                    f"Error checking {plant_name}: Water level "
                    f"{water_level} is too low (min 2)"
                )
            elif water_level > 10:
                raise WaterError(
                    f"Error checking {plant_name}: Water level "
                    f"{water_level} is too high (max 10)"
                )
            elif sunlight_hours < 2:
                raise GardenError(
                    f"Error checking {plant_name}: Sunlight hour"
                    f"s {sunlight_hours} are too low (min 2)"
                )
            elif sunlight_hours > 12:
                raise GardenError(
                    f"Error checking {plant_name}: Sunlight hour"
                    f"s {sunlight_hours} are too high (max 12)"
                )
            else:
                print(f"{plant_name}: healthy (water: {water_level}, "
                      f"sun: {sunlight_hours})")

        except GardenError as e:
            print(e)


def test_garden_management() -> None:
    """Run comprehensive tests for the garden management system."""
    gm = GardenManager()
    print("=== Garden Management System ===\n")

    print("Adding plants to garden...")
    gm.add_plants("tomato")
    gm.add_plants("lettuce")
    gm.add_plants(None)

    print("\nWatering plants...")
    gm.water_plants()

    print("\nChecking plant health...")
    gm.check_plant_health("tomato", 5, 8)
    gm.check_plant_health("lettuce", 15, 5)
    gm.check_plant_health("potato", 5, 0)
    gm.check_plant_health(None, 5, 0)

    print("\nTesting error recovery...")
    try:
        raise WaterError("Not enough water in tank")
    except GardenError as e:
        print(f"Caught Garden Error: {e}")
    finally:
        print("System recovered and continuing...")

    print("\nGarden management system test complete!")


if __name__ == "__main__":
    test_garden_management()
