#!/usr/bin/env python3


class Plant:
    """Base class for all garden plants."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a plant with name, height and age."""
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    """A flowering plant with a color attribute."""

    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        """Initialize a flower with name, height, age and color."""
        super().__init__(name, height, age)
        self.color = color

    def bloom(self) -> None:
        """Print a blooming message for this flower."""
        print(f"{self.name.capitalize()} is blooming beautifully!\n")

    def info(self) -> None:
        """Print the flower's details."""
        print(
            f"{self.name.capitalize()} (Flower): {self.height}cm, "
            f"{self.age} days, {self.color.lower()} color"
        )


class Tree(Plant):
    """A tree with a trunk diameter attribute."""

    def __init__(
        self, name: str, height: int, age: int, trunk_diameter: int
    ) -> None:
        """Initialize a tree with name, height, age and trunk diameter."""
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        """Print the estimated shade area for this tree."""
        print(
            f"{self.name.capitalize()} provides "
            f"{(((self.height / 100) ** 2) * 3.14):.0f} "
            f"square meters of shade\n"
        )

    def info(self) -> None:
        """Print the tree's details."""
        print(
            f"{self.name.capitalize()} (Tree): {self.height}cm,"
            f" {self.age} days, {self.trunk_diameter}cm diameter"
        )


class Vegetable(Plant):
    """An edible plant with harvest season and nutritional info."""

    def __init__(
        self,
        name: str,
        height: int,
        age: int,
        harvest_season: str,
        nutritional_value: str,
    ) -> None:
        """Initialize a vegetable with growing and nutritional details."""
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def rich(self) -> None:
        """Print the vegetable's nutritional highlight."""
        print(
            f"{self.name.capitalize()} is rich in {self.nutritional_value}!\n"
        )

    def info(self) -> None:
        """Print the vegetable's details."""
        print(
            f"{self.name.capitalize()} (Vegetable): {self.height}cm, "
            f"{self.age} days, {self.harvest_season.lower()} harvest"
        )


def main() -> None:
    """Create various plant types and display their info."""
    f1 = Flower("rose", 25, 30, "RED")
    f2 = Flower("sunflower", 25, 30, "yEllOw")
    t1 = Tree("oak", 500, 1825, 50)
    t2 = Tree("maple", 300, 1000, 50)
    v1 = Vegetable("tomato", 80, 90, "SuMMer", "vitamin C")
    v2 = Vegetable("potato", 70, 80, "wInTer", "potassium")

    flowers = [f1, f2]
    trees = [t1, t2]
    veggies = [v1, v2]

    print("=== Garden Plant Types ===\n")

    for f in flowers:
        f.info()
        f.bloom()

    for t in trees:
        t.info()
        t.produce_shade()

    for v in veggies:
        v.info()
        v.rich()


if __name__ == "__main__":
    main()
