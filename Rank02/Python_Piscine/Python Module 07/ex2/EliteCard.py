from ex0.Card import Card, CardType
from ex2.Magical import Magical
from ex2.Combatable import Combatable
from typing import Dict, List, Any


class EliteCard(Card, Magical, Combatable):
    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        combat_type: str,
        attack_pwr: int,
        defense_pwr: int,
        mana: int,
    ) -> None:
        super().__init__(name, cost, rarity)
        self.type = CardType.ELITE.value
        self.attack_pwr = attack_pwr
        self.defense_pwr = defense_pwr
        self.combat_type = combat_type
        self.mana = mana
        self.alive = True

    # ====== CARD ABC METHODS ======
    def play(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Slapped him or something",
        }

    def get_card_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "combat_type": self.combat_type,
            "attack_power": self.attack_pwr,
            "defense_power": self.defense_pwr,
        }

    # ====== COMBAT ABC METHODS ======
    def attack(self, target: Any) -> Dict[str, Any]:
        return {
            "attacker": self.name,
            "target": target,
            "damage": self.attack_pwr,
            "combat_type": self.combat_type,
        }

    def defend(self, incoming_damage: int) -> Dict[str, Any]:
        if incoming_damage > self.defense_pwr:
            self.alive = False
        return {
            "defender": self.name,
            "damage_taken": incoming_damage,
            "damage_blocked": self.defense_pwr,
            "still_alive": self.alive,
        }

    def get_combat_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "combat_type": self.combat_type,
            "attack_power": self.attack_pwr,
            "defense_power": self.defense_pwr,
        }

    # ====== MAGIC ABC METHODS ======
    def cast_spell(
        self, spell_name: str, targets: List[Any]
    ) -> Dict[str, Any]:
        return {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": self.cost,
        }

    def channel_mana(self, amount: int) -> Dict[str, Any]:
        total_mana = self.mana - amount
        return {"channeled": amount, "total_mana": total_mana}

    def get_magic_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "base_mana": self.mana,
        }
