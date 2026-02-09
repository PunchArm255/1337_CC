#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: int, age_: int):
        self.name = name
        self.height = height
        self.age_ = age_

    def grow(self):
        self.height += 1

    def age(self):
        self.age_ += 1

    def get_info(self):
        print(f"{self.name}: {self.height}cm {self.age_} days old")


def main():
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
