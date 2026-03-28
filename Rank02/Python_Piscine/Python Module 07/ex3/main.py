from ex0.CreatureCard import CreatureCard
from ex0.Card import CardRarity
from ex1.SpellCard import SpellCard
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.GameEngine import GameEngine


def main() -> None:
    try:
        print("\n=== DataDeck Game Engine ===")

        factory = FantasyCardFactory()
        strategy = AggressiveStrategy()
        engine = GameEngine()
        engine.configure_engine(factory, strategy)

        card1 = CreatureCard(
            "Fire Dragon", 5, CardRarity.LEGENDARY.value, 7, 5
        )
        card2 = CreatureCard(
            "Goblin Warrior", 2, CardRarity.COMMON.value, 7, 5
        )
        card3 = SpellCard(
            "Lightning Bolt", 3, CardRarity.RARE.value, "Deal damage"
        )

        print("\nConfiguring Fantasy Card Game...")
        print(f"Factory: {factory.__class__.__name__}")
        print(f"Strategy: {strategy.get_strategy_name()}")
        print(f"Available types: {factory.get_supported_types()}")

        print("\nSimulating aggressive turn...")
        print(
            f"Hand: [{card1.name} ({card1.cost}, {card2.name} ({card2.cost}),"
            f" {card3.name} ({card3.cost})]"
        )

        print("\nTurns execution:")
        print(f"Strategy: {strategy.get_strategy_name()}")
        print(
            f"Actions: "
            f"{strategy.execute_turn([card2, card3], ["Enemy Player"])}"
        )

        print("\nGame Report:")
        print(engine.simulate_turn())

        print(
            "\nAbstract Factory + Strategy Pattern: "
            "Maximum flexibility achieved!"
        )

    except Exception as e:
        print(f"\nERROR: Invalid Syntax. Check the type hints!\nDETAILS: {e}")


if __name__ == "__main__":
    main()
