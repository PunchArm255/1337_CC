from ex2.EliteCard import EliteCard


def main():
    print("\n=== DataDeck Ability System ===\n")

    print("=== DataDeck Ability System ===")
    print("EliteCard capabilities:")
    print("- Card: ['play', 'get_card_info', 'is_playable']")
    print("- Combatable: ['attack', 'defend', 'get_combat_stats']")
    print("- Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']")

    card1 = EliteCard("Arcane Warrior", 4, "Legendary", "Melee", 5, 3, 10)

    print(f"\nPlaying {card1.name} ({card1.type} Card):")

    print("\nCombat phase:")
    print(f"Attack result: {card1.attack("Enemy")}")
    print(f"Defense attack: {card1.defend(99)}")

    print("\nMagic phase:")
    print(f"Spell cast: {card1.cast_spell("Fireball", ["Enemy1", "Enemy2"])}")
    print(f"Mana channel: {card1.channel_mana(3)}")

    print("\nMultiple interface implementation successful!")

    # print("\n============ OTHER TESTS ============")
    # print(f"\nplay(): {card1.play({})}")
    # print(f"\nget_card_info(): {card1.get_card_info()}")
    # print(f"\nis_playable: {card1.is_playable(5)}")
    # print(f"\nget_combat_stats(): {card1.get_combat_stats()}")
    # print(f"\nget_magic_stats(): {card1.get_magic_stats()}")


if __name__ == "__main__":
    main()