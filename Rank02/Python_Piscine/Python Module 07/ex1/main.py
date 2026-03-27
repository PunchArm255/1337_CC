from ex0.CreatureCard import CreatureCard
from ex0.Card import CardRarirty
from ex1.Deck import Deck
from ex1.ArtifactCard import ArtifactCard
from ex1.SpellCard import SpellCard


def main():
    print("\n=== DataDeck Deck Builder ===")
    print("\nBuilding deck with different card types...")

    deck = Deck()
    card1 = SpellCard("Lightning Bolt", 3, "Rare", "Deal 3 damage to target")
    card2 = ArtifactCard("Mana Crystal", 2, "Common", 7, "Permanent: +1 mana per turn")
    card3 = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    deck.add_card(card1)
    deck.add_card(card2)
    deck.add_card(card3)
    print(f"Deck stats: {deck.get_deck_stats()}")

    print("\nDrawing and playing cards:")

    print(f"\nDrew: {card1.name} ({card1.type})")
    print(f"Play result: {card1.play({})}")

    print(f"\nDrew: {card2.name} ({card2.type})")
    print(f"Play result: {card2.play({})}")

    print(f"\nDrew: {card3.name} ({card3.type})")
    print(f"Play result: {card3.play({})}")

    print("\nPolymorphism in action: Same interface, different card behaviors!")


if __name__ == "__main__":
    main()
