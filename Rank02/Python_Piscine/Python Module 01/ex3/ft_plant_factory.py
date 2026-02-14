#!/usr/bin/env python3


class Plant:
    """Represent a plant created by the factory."""

    def __init__(self, name: str, height: int, age_: int) -> None:
        """Initialize a plant with name, height and age."""
        self.name = name
        self.height = height
        self.age_ = age_

    def get_info(self) -> None:
        """Print the plant's creation details."""
        print(f"Created: {self.name} ({self.height}cm, {self.age_} days)")


def main() -> None:
    """Create multiple plants and display the factory output."""
    plants = []
    plants.append(Plant("Rose", 25, 30))
    plants.append(Plant("Sunflower", 80, 45))
    plants.append(Plant("Cactus", 5, 90))
    plants.append(Plant("Oak", 200, 365))
    plants.append(Plant("Fern", 15, 120))

    print("=== Plant Factory Output ===")
    for i in range(0, 5):
        plants[i].get_info()
    print(f"\nTotal plants created: {i+1}")


if __name__ == "__main__":
    main()
