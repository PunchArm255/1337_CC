from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable

class TournamentCard(Card, Combatable, Rankable):
    def __init__(self, name: str, cost: int, rarity: str, attack_pwr: int, defense_pwr: int, initial_rating: int):
        super().__init__(name, cost, rarity)
        self.attack_pwr = attack_pwr
        self.defense_pwr = defense_pwr
        self.rating = initial_rating
        self.wins = 0
        self.losses = 0

    # ====== CARD ABC METHODS ======
    def play(self, game_state: dict) -> dict:
        return {"card_played": self.name, "effect": "Entered tournament"}

    # ====== COMBAT ABC METHODS ======
    def attack(self, target: str) -> dict:
        return {"attacker": self.name, "target": target, "damage": self.attack_pwr}

    def defend(self, incoming_damage: int) -> dict:
        dmg_taken = max(0, incoming_damage - self.defense_pwr)
        return {"defender": self.name, "damage_taken": dmg_taken}

    def get_combat_stats(self) -> dict:
        return {"attack": self.attack_pwr, "block": self.defense_pwr}

    # ====== RANKING ABC METHODS ======
    def calculate_rating(self) -> int:
        return self.rating

    def update_wins(self, wins: int) -> None:
        self.wins += wins

    def update_losses(self, losses: int) -> None:
        self.losses += losses

    def get_rank_info(self) -> dict:
        return {"rating": self.rating, "wins": self.wins, "losses": self.losses}

    # ====== OWN METHODS ======
    def get_tournament_stats(self) -> dict:
        return {
            "rating": self.rating,
            "record": f"{self.wins}-{self.losses}"
        }
