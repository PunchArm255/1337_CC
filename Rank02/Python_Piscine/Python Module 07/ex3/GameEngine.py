from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy
from typing import Dict, Any, Optional


class GameEngine:
    def __init__(self) -> None:
        self.factory: Optional[CardFactory] = None
        self.strategy: Optional[GameStrategy] = None
        self.turns = 0

    def configure_engine(
        self, factory: CardFactory, strategy: GameStrategy
    ) -> None:
        self.factory = factory
        self.strategy = strategy

    def simulate_turn(self) -> Dict[str, Any]:
        self.turns += 1
        cards = ["Goblin Warrior", "Lightning Bolt"]
        field_enemies = ["Enemy Player"]

        execute_result = self.strategy.execute_turn(
            cards, field_enemies
        )

        return {
            "turns_simulated": self.turns,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": execute_result["damage_dealt"],
            "cards_played": len(cards),
        }

    def get_engine_status(self) -> Dict[str, Any]:
        return {
            "factory": (
                self.factory.__class__.__name__ if self.factory else None
            ),
            "strategy": (
                self.strategy.get_strategy_name() if self.strategy else None
            ),
        }
