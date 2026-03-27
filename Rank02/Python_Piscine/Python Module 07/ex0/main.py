from ex0.CreatureCard import CreatureCard


def main():
    print("\n=== DataDeck Card Foundation ===")
    print("\nTesting Abstract Base Class Design:")

    print("\nCreatureCard Info:")
    dragon = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    mana = 6
    print(dragon.get_card_info())

    print(f"\nPlaying {dragon.name} with {mana} mana available:")
    print(f"Playable: {dragon.is_playable(mana)}")
    if dragon.is_playable(mana):
        print(f"Play result: {dragon.play({})}")

    print(f"\n{dragon.name} attacks Goblin Warrior:")
    print(f"Attack result: {dragon.attack_target("Goblin Warrior")}")

    mana = 3
    print(f"Testing insufficient mana ({mana} available):")
    print(f"Playable: {dragon.is_playable(mana)}")

    print("\nAbstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()