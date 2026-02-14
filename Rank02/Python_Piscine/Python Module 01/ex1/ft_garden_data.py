#!/usr/bin/env python3


class Plant:
    """Represent a garden plant with basic attributes."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a plant with name, height and age."""
        self.name = name
        self.height = height
        self.age = age


def main() -> None:
    """Create plants and display the garden registry."""
    p1 = Plant("Rose", 25, 30)
    p2 = Plant("Sunflower", 80, 45)
    p3 = Plant("Cactus", 15, 120)
    plant_list = [p1, p2, p3]
    print("=== Garden Plant Registry ===")
    for p in plant_list:
        print(f"{p.name}: {p.height}cm, {p.age} days old")


if __name__ == "__main__":
    main()
