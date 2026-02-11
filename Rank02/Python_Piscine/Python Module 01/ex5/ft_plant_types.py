#!/usr/bin/env python3


class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        print(f"{self.name.capitalize()} is blooming beautifully!\n")

    def info(self):
        print(
            f"{self.name.capitalize()} (Flower): {self.height}cm, {self.age} days, {self.color.lower()} color"
        )


class Tree(Plant):
    def __init__(self, name: str, height: int, age: int, trunk_diameter: int):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self):
        print(
            f"{self.name.capitalize()} provides {int(((self.height / 100) ** 2) * 3.14)} square meters of shade\n"
        )

    def info(self):
        print(
            f"{self.name.capitalize()} (Tree): {self.height}cm, {self.age} days, {self.trunk_diameter}cm diameter"
        )


class Vegetable(Plant):
    def __init__(
        self,
        name: str,
        height: int,
        age: int,
        harvest_season: str,
        nutritional_value: str,
    ):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def rich(self):
        print(
            f"{self.name.capitalize()} is rich in {self.nutritional_value}!\n"
        )

    def info(self):
        print(
            f"{self.name.capitalize()} (Vegetable): {self.height}cm, {self.age} days, {self.harvest_season.lower()} harvest"
        )


def main():
    f1 = Flower("rose", 25, 30, "RED")
    t1 = Tree("oak", 500, 1825, 50)
    v1 = Vegetable("tomato", 80, 90, "SuMMer", "vitamin C")

    print("=== Garden Plant Types ===\n")

    f1.info()
    f1.bloom()

    t1.info()
    t1.produce_shade()

    v1.info()
    v1.rich()


if __name__ == "__main__":
    main()
