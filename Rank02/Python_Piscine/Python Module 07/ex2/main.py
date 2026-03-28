from ex2.EliteCard import EliteCard
from ex0.Card import CardRarity


def main() -> None:
    try:
        print("\n=== DataDeck Ability System ===\n")

        print("=== DataDeck Ability System ===")
        print("EliteCard capabilities:")
        print("- Card: ['play', 'get_card_info', 'is_playable']")
        print("- Combatable: ['attack', 'defend', 'get_combat_stats']")
        print("- Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']")

        card1 = EliteCard(
            "Arcane Warrior", 4, CardRarity.LEGENDARY.value, "Melee", 5, 3, 10
        )

        print(f"\nPlaying {card1.name} ({card1.type} Card):")

        print("\nCombat phase:")
        print(f"Attack result: {card1.attack("Enemy")}")
        print(f"Defense attack: {card1.defend(5)}")

        print("\nMagic phase:")
        print(f"Spell cast: "
              f"{card1.cast_spell("Fireball", ["Enemy1", "Enemy2"])}")
        print(f"Mana channel: {card1.channel_mana(3)}")

        print("\nMultiple interface implementation successful!")

    except Exception as e:
        print(f"\nERROR: Invalid Syntax. Check the type hints!\nDETAILS: {e}")


if __name__ == "__main__":
    main()
