from ex4.TournamentCard import TournamentCard
from typing import Dict, List, Any


class TournamentPlatform:
    def __init__(self) -> None:
        self.cards: Dict[str, TournamentCard] = {}
        self.winner_id = ""
        self.loser_id = ""
        self.matches_played = 0

    def register_card(self, card: TournamentCard) -> str:
        card_id = f"{card.name}_001"
        self.cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> Dict[str, Any]:
        self.matches_played += 1
        c1 = self.cards[card1_id]
        c2 = self.cards[card2_id]

        attack_data = c1.attack(c2.name)
        defense_data = c2.defend(attack_data["damage"])

        if defense_data["damage_taken"] > 0:
            winner, loser = c1, c2
            self.winner_id, self.loser_id = card1_id, card2_id
        else:
            winner, loser = c2, c1
            self.winner_id, self.loser_id = card2_id, card1_id

        winner.update_wins(1)
        loser.update_losses(1)

        winner.rating += 16
        loser.rating -= 16

        return {
            "winner": self.winner_id,
            "loser": self.loser_id,
            "winner_rating": c1.rating,
            "loser_rating": c2.rating,
        }

    def get_leaderboard(self) -> List[str]:
        w_name = self.cards[self.winner_id].name
        l_name = self.cards[self.loser_id].name
        w_rating = self.cards[self.winner_id].rating
        l_rating = self.cards[self.loser_id].rating
        w_wins = self.cards[self.winner_id].wins
        l_wins = self.cards[self.loser_id].wins
        w_losses = self.cards[self.winner_id].losses
        l_losses = self.cards[self.loser_id].losses
        if w_rating > l_rating:
            return [
                f"1. {w_name} - Rating: {w_rating} ({w_wins}-{w_losses})",
                f"2. {l_name} - Rating: {l_rating} ({l_wins}-{l_losses})",
            ]
        else:
            return [
                f"1. {l_name} - Rating: {l_rating} ({l_wins}-{l_losses})",
                f"2. {w_name} - Rating: {w_rating} ({w_wins}-{w_losses})",
            ]

    def generate_tournament_report(self) -> Dict[str, Any]:
        total_rating = sum(c.rating for c in self.cards.values())
        avg = int(total_rating / len(self.cards)) if self.cards else 0

        return {
            "total_cards": len(self.cards),
            "matches_played": self.matches_played,
            "avg_rating": avg,
            "platform_status": "active",
        }
