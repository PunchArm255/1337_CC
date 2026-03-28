from ex4.TournamentPlatform import TournamentPlatform
from ex4.TournamentCard import TournamentCard
from ex0.Card import CardRarity


def main() -> None:
    try:
        print("\n=== DataDeck Tournament Platform ===")

        print("\nRegistering Tournament Cards...")
        platform = TournamentPlatform()
        card1 = TournamentCard(
            "Fire Dragon", 5, CardRarity.LEGENDARY.value, 7, 5, 1200
        )
        card2 = TournamentCard(
            "Ice Wizard", 3, CardRarity.RARE.value, 4, 2, 1150
        )
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
        print("\n".join(platform.get_leaderboard()))

        print("\nPlatform Report:")
        print(platform.generate_tournament_report())

        print("\n=== Tournament Platform Successfully Deployed! ===")
        print("All abstract patterns working together harmoniously!")

    except Exception as e:
        print(f"\nERROR: Invalid Syntax. Check the type hints!\nDETAILS: {e}")


if __name__ == "__main__":
    main()
