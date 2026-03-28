from typing import Dict, Any
from ex0.Card import Card, CardType


class ArtifactCard(Card):
    def __init__(
        self, name: str, cost: int, rarity: str, durability: int, effect: str
    ) -> None:
        super().__init__(name, cost, rarity)
        self.type = CardType.ARTIFACT.value
        self.durability = durability
        self.effect = effect

    def play(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": self.effect,
        }

    def activate_ability(self) -> Dict[str, Any]:
        self.durability -= 1
        return {
            "artifact": self.name,
            "durability_left": self.durability,
            "status": "activated",
        }
