#!/usr/bin/env python3

from typing import List


class GardenManager:
    """Manage a garden of plants with stats tracking."""

    class GardenStats:
        """Track statistics for a single garden."""

        def __init__(self) -> None:
            """Initialize all stat counters to zero."""
            self.plants: int = 0
            self.flowering: int = 0
            self.prize: int = 0
            self.growth: int = 0

        def calc_score(self, plant_list: List['Plant']) -> int:
            """Return total score of all plants in the list."""
            score = 0
            for plant in plant_list:
                score += plant.get_score()
            return score

        def stat_report(self, validation: bool) -> None:
            """Print garden scores and validation status."""
            print(f"Height validation test: {validation}")

            scores = []
            for gm in GardenManager.garden_list:
                sc = gm.stats.calc_score(gm.plant_list)
                scores.append(f"{gm.owner}: {sc}")
            print(f"Garden scores - {', '.join(scores)}")
            print(f"Total gardens managed: {GardenManager.gardens}")

        def plant_types(self) -> None:
            """Print a summary of plant type counts and growth."""
            total = self.plants + self.flowering + self.prize
            print(f"\nPlants added: {total}, Total growth: {self.growth}cm")
            print(
                f"Plant types: {self.plants} regular, "
                f"{self.flowering} flowering, {self.prize} prize flowers\n"
            )

    gardens: int = 0
    garden_list: List['GardenManager'] = []

    def __init__(self, owner: str) -> None:
        """Initialize a garden for the given owner."""
        self.owner = owner
        self.plant_list: List['Plant'] = []
        self.stats = self.GardenStats()
        self.validation = True
        GardenManager.gardens += 1
        GardenManager.garden_list.append(self)

    @classmethod
    def create_garden_network(cls) -> None:
        """Print the garden management system header."""
        print("=== Garden Management System Demo ===\n")

    @staticmethod
    def height_validation(height: int) -> bool:
        """Return True if height is non-negative."""
        return height >= 0

    def add_plant(self, name: str, height: int, age: int) -> None:
        """Add a regular plant to the garden."""
        if not GardenManager.height_validation(height):
            self.validation = False
            print(f"Cannot add {name}. [HEIGHT IS NEGATIVE]")
        else:
            new_plant = Plant(name, height, age)
            self.plant_list.append(new_plant)
            print(f"Added {name} to {self.owner}'s garden")
            self.stats.plants += 1

    def add_flowering_plant(
        self, name: str, height: int, age: int, color: str
    ) -> None:
        """Add a flowering plant to the garden."""
        if not GardenManager.height_validation(height):
            self.validation = False
            print(f"Cannot add {name}. [HEIGHT IS NEGATIVE]")
        else:
            new_plant = FloweringPlant(name, height, age, color)
            self.plant_list.append(new_plant)
            print(f"Added {name} to {self.owner}'s garden")
            self.stats.flowering += 1

    def add_prize_flower(
        self, name: str, height: int, age: int, color: str, prize: int
    ) -> None:
        """Add a prize flower to the garden."""
        if not GardenManager.height_validation(height):
            self.validation = False
            print(f"Cannot add {name}. [HEIGHT IS NEGATIVE]")
        else:
            new_plant = PrizeFlower(name, height, age, color, prize)
            self.plant_list.append(new_plant)
            print(f"Added {name} to {self.owner}'s garden")
            self.stats.prize += 1

    def grow_all(self) -> None:
        """Grow all plants in the garden by 1cm each."""
        print(f"\n{self.owner} is helping all plants grow...")
        for plant in self.plant_list:
            plant.grow()
            self.stats.growth += 1

    def all_stats(self) -> None:
        """Print a full report for this garden."""
        print(f"\n=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plant_list:
            plant.get_info()
        self.stats.plant_types()
        self.stats.stat_report(self.validation)


class Plant:
    """Represent a basic garden plant."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a plant with name, height and age."""
        self.name = name
        self.height = height
        self.age = age

    def grow(self) -> None:
        """Increase the plant's height by 1cm."""
        self.height += 1
        print(f"{self.name} grew 1cm")

    def get_info(self) -> None:
        """Print the plant's name and height."""
        print(f"- {self.name}: {self.height}cm")

    def get_score(self) -> int:
        """Return the plant's score based on height."""
        return self.height


class FloweringPlant(Plant):
    """A plant that produces colored flowers."""

    def __init__(
        self, name: str, height: int, age: int, color: str
    ) -> None:
        """Initialize a flowering plant with a color."""
        super().__init__(name, height, age)
        self.color = color

    def get_info(self) -> None:
        """Print the flowering plant's details."""
        print(
            f"- {self.name}: {self.height}cm, {self.color} flowers (blooming)"
        )

    def get_score(self) -> int:
        """Return score with a flowering bonus."""
        return super().get_score() + 15


class PrizeFlower(FloweringPlant):
    """A flowering plant that has won prize points."""

    def __init__(
        self, name: str, height: int, age: int, color: str, points: int
    ) -> None:
        """Initialize a prize flower with prize points."""
        super().__init__(name, height, age, color)
        self.points = points

    def get_info(self) -> None:
        """Print the prize flower's details including points."""
        print(
            f"- {self.name}: {self.height}cm, {self.color} flowers (blooming),"
            f" Prize points: {self.points}"
        )

    def get_score(self) -> int:
        """Return score with prize point bonus."""
        return super().get_score() + self.points


def main() -> None:
    """Demo the full garden management system."""
    GardenManager.create_garden_network()

    gm1 = GardenManager("Alice")

    gm1.add_plant("Oak Tree", 100, 100)
    gm1.add_flowering_plant("Rose", 25, 60, "red")
    gm1.add_prize_flower("Sunflower", 50, 40, "yellow", 10)

    gm1.grow_all()

    gm1.all_stats()


if __name__ == "__main__":
    main()
