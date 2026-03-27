from ex4.TournamentPlatform import TournamentPlatform
from ex4.TournamentCard import TournamentCard

def main():
    print("\n=== DataDeck Tournament Platform ===")

    print("\nRegistering Tournament Cards...")
    platform = TournamentPlatform()
    card1 = TournamentCard("Fire Dragon", 5, "Legendary", 7, 5, 1200)
    card2 = TournamentCard("Ice Wizard", 3, "Rare", 4, 2, 1150)
    dragon_id = platform.register_card(card1)
    wizard_id = platform.register_card(card2)

    print(f"\n{card1.name} (ID: {dragon_id}):")
    print("- Interface: [Card, Combatable, Rankable]")
    print(f"- Ranking: {card1.rating}")
    print(f"- Record: {card1.wins}-{card1.losses}")

    print(f"\n{card2.name} (ID: {wizard_id}):")
    print("- Interface: [Card, Combatable, Rankable]")
    print(f"- Ranking: {card2.rating}")
    print(f"- Record: {card2.wins}-{card2.losses}")

    print("\nCreating tournament match...")
    print(f"Match result: {platform.create_match(dragon_id, wizard_id)}")

    print("\nTournament Leaderboard:")
    print(f"1. {card1.name} - Rating: {card1.rating} ({card1.wins}-{card1.losses})")
    print(f"2. {card2.name} - Rating: {card2.rating} ({card2.wins}-{card2.losses})")

    print("\nPlatform Report:")
    print(platform.generate_tournament_report())





if __name__ == "__main__":
    main()