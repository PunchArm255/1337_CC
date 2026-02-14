#!/usr/bin/env python3


class Plant:
    """Represent a plant that can grow and age over time."""

    def __init__(self, name: str, height: int, age_: int) -> None:
        """Initialize a plant with name, height and age."""
        self.name = name
        self.height = height
        self.age_ = age_

    def grow(self) -> None:
        """Increase the plant's height by 1cm."""
        self.height += 1

    def age(self) -> None:
        """Increase the plant's age by 1 day."""
        self.age_ += 1

    def get_info(self) -> None:
        """Print the plant's current height and age."""
        print(f"{self.name}: {self.height}cm {self.age_} days old")


def main() -> None:
    """Simulate a week of plant growth and display daily progress."""
    p1 = Plant("Rose", 25, 30)

    for i in range(1, 8):
        print(f"=== Day {i} ===")
        p1.get_info()
        if i == 7:
            print("Growth this week: +6cm")
        p1.grow()
        p1.age()


if __name__ == "__main__":
    main()
