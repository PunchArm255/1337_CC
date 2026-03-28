from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any


class CardType(Enum):
    CREATURE = "Creature"
    SPELL = "Spell"
    ARTIFACT = "Artifact"
    ELITE = "Elite"


class CardRarity(Enum):
    COMMON = "Common"
    RARE = "Rare"
    LEGENDARY = "Legendary"


class Card(ABC):
    def __init__(self, name: str, cost: int, rarity: str) -> None:
        self.name = name
        self.cost = cost
        self.rarity = rarity

    @abstractmethod
    def play(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def get_card_info(self) -> Dict[str, Any]:
        return {"name": self.name, "cost": self.cost, "rarity": self.rarity}

    def is_playable(self, available_mana: int) -> bool:
        return self.cost <= available_mana
