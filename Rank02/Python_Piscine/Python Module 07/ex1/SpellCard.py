from ex0.Card import Card, CardRarirty, CardType

class SpellCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        super().__init__(name, cost, rarity)
        self.type = CardType.SPELL.value
        self.effect_type = effect_type
        self.consumed = False

    def play(self, game_state: dict) -> dict:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": self.effect_type
        }

    def resolve_effect(self, targets: list) -> dict:
        if self.consumed is False:
            self.consumed = True
            return {
                "spell": self.name,
                "targets": targets,
                "status": "resolved"
            }
        else:
            return {
                "spell": self.name,
                "targets": targets,
                "status": "cannot resolve, spell already consumed."
            }