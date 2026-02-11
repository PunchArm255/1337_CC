#!/usr/bin/env python3

class SecurePlant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self._height = height
        self._age = age
    def get_info(self):
        print(f"Current plant: {self.name} ({self._height}cm, {self._age} days)")

    # getters diali
    def get_height(self):
        return self._height

    def get_age(self):
        return self._age

    # setters diali
    def set_height(self, height):
        if height >= 0:
            self._height = height
            print(f"Height updated: {self._height}cm [OK]")
        else:
            print(f"\nInvalid operation attempted: height -{self._height}cm [REJECTED]")
            print("Security: Negative height rejected\n")

    def set_age(self, age):
        if age >= 0:
            self._age = age
            print(f"Height updated: {self._age} days [OK]")
        else:
            print(f"\nInvalid operation attempted: age -{self._age} days [REJECTED]")
            print("Security: Negative age rejected\n")


def main():
    p1 = SecurePlant("Rose", 25, 30)
    print("=== Garden Security System ===")
    print(f"Plant created: {p1.name}")

    p1.set_height(61)
    p1.set_age(70)

    p1.set_height(-60)
    p1.set_age(-100)

    p1.get_info()


if __name__ == "__main__":
    main()
