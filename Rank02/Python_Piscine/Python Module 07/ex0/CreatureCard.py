from typing import Dict, Any
from ex0.Card import Card, CardType


class CreatureCard(Card):
    def __init__(
        self, name: str, cost: int, rarity: str, attack: int, health: int
    ) -> None:
        super().__init__(name, cost, rarity)
        self.type = CardType.CREATURE.value
        self.attack = attack
        self.health = health

        if not isinstance(attack, int) or attack < 0:
            raise ValueError("[ERROR] Attack value must be a positive integer")
        if not isinstance(health, int) or health < 0:
            raise ValueError("[ERROR] Health value must be a positive integer")

    def play(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield",
        }

    def attack_target(self, target: Any) -> Dict[str, Any]:
        return {
            "attacker": self.name,
            "target": target,
            "damage_dealt": self.attack,
            "combat_resolved": True,
        }

    def get_card_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "type": self.type,
            "attack": self.attack,
            "health": self.health,
        }
