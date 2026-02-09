#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: int, age_: int):
        self.name = name
        self.height = height
        self.age_ = age_

    def get_info(self):
        print(f"Created: {self.name} ({self.height}cm, {self.age_} days)")

