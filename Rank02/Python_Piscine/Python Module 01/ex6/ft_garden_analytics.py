#!/usr/bin/env python3

class GardenManager:
    
    plants = 0
    flowering = 0
    prize = 0
    growth = 0
    gardens = 0
    validation = True
    garden_list = []

    def __init__(self, owner):
        self.owner = owner
        self.plant_list = []
        GardenManager.gardens += 1
        GardenManager.garden_list.append(self)

    @classmethod
    def create_garden_network(cls):
        print("=== Garden Management System Demo ===")

    def add_plant(self, name, height, age):
        if height < 0:
            self.validation = False
        new_plant = Plant(name, height, age)
        self.plant_list.append(new_plant)
        print(f"Added {name} to {self.owner}'s garden")
        self.plants += 1
    
    def add_flowering_plant(self, name, height, age, color):
        if height < 0:
            self.validation = False
        new_plant = FloweringPlant(name, height, age, color)
        self.plant_list.append(new_plant)
        print(f"Added {name} to {self.owner}'s garden")
        self.flowering += 1
    
    def add_prize_flower(self, name, height, age, color, prize):
        if height < 0:
            self.validation = False
        new_plant = PrizeFlower(name, height, age, color, prize)
        self.plant_list.append(new_plant)
        print(f"Added {name} to {self.owner}'s garden")
        self.prize += 1
    
    def grow_all(self):
        print(f"\n{self.owner} is helping all plants grow...")
        for plant in self.plant_list:
            plant.grow()
            self.growth += 1

    def all_stats(self):
        for plant in self.plant_list:
            plant.get_info()
        print(f"\nPlants added: {self.plants + self.flowering + self.prize}, Total growth: {self.growth}cm")
        print(f"Plant types: {self.plants} regular, {self.flowering} flowering, {self.prize} prize flowers\n")
        print(f"Height validation test: {self.validation}")
        scores = []
        for gm in GardenManager.garden_list:
            scores.append(f"{gm.owner}: {gm.calc_score()}")
        print(f"Garden scores - {', '.join(scores)}")
        print(f"Total gardens managed: {self.gardens}")
    
    def calc_score(self):
        score = 0
        for plant in self.plant_list:
            score += plant.get_score()
        return score


class Plant:

    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age

    def grow(self):
        self.height += 1
        print(f"{self.name} grew 1cm")

    def age(self):
        self.age_ += 1
    
    def get_info(self):
        print(f"- {self.name}: {self.height}cm")
    
    def get_score(self):
        return self.height


class FloweringPlant(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def get_info(self):
        print(f"- {self.name}: {self.height}cm, {self.color} flowers (blooming)")

    def get_score(self):
        return super().get_score() + 15

class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, age, color, points):
        super().__init__(name, height, age, color)
        self.points = points

    def get_info(self):
        print(f"- {self.name}: {self.height}cm, {self.color} flowers (blooming), Prize points: {self.points}")

    def get_score(self):
        return super().get_score() + self.points

def main():
    gm1 = GardenManager("Alice")
    gm2 = GardenManager("IDK")
    gm3 = GardenManager("IDFK")
    print("=== Garden Management System Demo ===\n")
    gm1.add_plant("Oak Tree", 100, 100)
    gm1.add_flowering_plant("Rose", 24, 60, "red")
    gm1.add_prize_flower("Sunflower", 50, 40, "yellow", 10)
    gm1.grow_all()
    print("\n=== Alice's Garden Report ===")
    gm1.all_stats()


if __name__ == "__main__":
    main()
