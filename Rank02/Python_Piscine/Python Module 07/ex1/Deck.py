from ex0.Card import Card, CardType
from typing import Dict, List, Any
import random


class Deck:
    card_list: List[Card] = []

    def add_card(self, card: Card) -> None:
        self.card_list.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self.card_list:
            if card.name == card_name:
                self.card_list.remove(card)
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self.card_list)

    def draw_card(self) -> Card:
        return random.choice(self.card_list)

    def get_deck_stats(self) -> Dict[str, Any]:
        creatures = [
            c for c in self.card_list if c.type == CardType.CREATURE.value
        ]
        spells = [c for c in self.card_list if c.type == CardType.SPELL.value]
        artifacts = [
            c for c in self.card_list if c.type == CardType.ARTIFACT.value
        ]
        avg = (
            sum(c.cost for c in self.card_list) / len(self.card_list)
            if len(self.card_list) != 0
            else 0.0
        )
        return {
            "total_card": len(self.card_list),
            "creatures": len(creatures),
            "spells": len(spells),
            "artifacts": len(artifacts),
            "avg_cost": f"{avg:.1f}",
        }
