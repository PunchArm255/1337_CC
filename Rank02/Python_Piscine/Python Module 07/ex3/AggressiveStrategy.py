from ex3.GameStrategy import GameStrategy
from ex0.CreatureCard import CreatureCard
from ex0.Card import Card
from typing import Dict, List, Any


class AggressiveStrategy(GameStrategy):
    def execute_turn(
        self, hand: List[Any], battlefield: List[Any]
    ) -> Dict[str, Any]:
        cards_played = [card.name for card in hand if isinstance(card, Card)]
        mana_used = [card.cost for card in hand if isinstance(card, Card)]
        dmg_dealt = [
            card.attack for card in hand if isinstance(card, CreatureCard)
        ]
        return {
            "cards_played": cards_played,
            "mana_used": sum(mana_used),
            "targets_attacked": self.prioritize_targets(battlefield),
            "damage_dealt": sum(dmg_dealt),
        }

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: List[Any]) -> List[Any]:
        return available_targets
