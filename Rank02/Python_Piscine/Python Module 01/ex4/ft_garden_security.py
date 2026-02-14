#!/usr/bin/env python3


class SecurePlant:
    """Represent a plant with validated access to its attributes."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a secure plant with name, height and age."""
        self.name = name
        self._height = height
        self._age = age

    def get_info(self) -> None:
        """Print the plant's current details."""
        print(f"Current plant: "
              f"{self.name} ({self._height}cm, {self._age} days)")

    # getters
    def get_height(self) -> int:
        """Return the plant's height."""
        return self._height

    def get_age(self) -> int:
        """Return the plant's age."""
        return self._age

    # setters
    def set_height(self, height: int) -> None:
        """Set height if non-negative, reject otherwise."""
        if height >= 0:
            self._height = height
            print(f"Height updated: {self._height}cm [OK]")
        else:
            print(f"\nInvalid operation attempted: height"
                  f" {height}cm [REJECTED]")
            print("Security: Negative height rejected\n")

    def set_age(self, age: int) -> None:
        """Set age if non-negative, reject otherwise."""
        if age >= 0:
            self._age = age
            print(f"Age updated: {self._age} days [OK]")
        else:
            print(f"\nInvalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected\n")


def main() -> None:
    """Demo the garden security system with valid and invalid inputs."""
    p1 = SecurePlant("Rose", 25, 30)
    print("=== Garden Security System ===")
    print(f"Plant created: {p1.name}")

    p1.set_height(100)
    p1.set_age(70)

    p1.set_height(-20)
    p1.set_age(-77)

    p1.get_info()


if __name__ == "__main__":
    main()
