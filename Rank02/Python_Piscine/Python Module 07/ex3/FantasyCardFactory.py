from ex3.CardFactory import CardFactory
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard

class FantasyCardFactory(CardFactory):
    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        return CreatureCard(name_or_power, 2, "Common", 2, 2)

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        return SpellCard(name_or_power, 3, "Rare", "Deal damage")

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        return ArtifactCard(name_or_power, 1, "Legendary", 3, "Mana boost")

    def create_themed_deck(self, size: int) -> dict:
        return {"deck_size": size, "theme": "Fantasy"}

    def get_supported_types(self) -> dict:
        return {
            'creatures': ['dragon', 'goblin'],
            'spells': ['fireball', 'iceball', 'lightning bolt'],
            'artifacts': ['mana_ring', 'mana_staff', 'mana_crystal']
        }
