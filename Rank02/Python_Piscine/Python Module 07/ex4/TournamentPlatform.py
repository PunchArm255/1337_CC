from ex4.TournamentCard import TournamentCard
from ex4.Rankable import Rankable

class TournamentPlatform:
    def __init__(self):
        self.cards = {}
        self.matches_played = 0

    def register_card(self, card: TournamentCard) -> str:
        card_id = f"{card.name}_001"    
        self.cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        self.matches_played += 1
        c1 = self.cards[card1_id]
        c2 = self.cards[card2_id]

        attack_data = c1.attack(c2.name)
        defense_data = c2.defend(attack_data["damage"])

        if defense_data["damage_taken"] > 0:
            winner, loser = c1, c2
            winner_id, loser_id = card1_id, card2_id
        else:
            winner, loser = c2, c1
            winner_id, loser_id = card2_id, card1_id
            
        winner.update_wins(1)
        loser.update_losses(1)
        
        winner.rating += 16
        loser.rating -= 16
        
        return {
            'winner': winner_id,
            'loser': loser_id,
            'winner_rating': c1.rating,
            'loser_rating': c2.rating
        }

    def get_leaderboard(self) -> list:
        return [
            f"{c1.name} - Rating: {card1.rating} ({card1.wins}-{card1.losses})",
            f"{card2.name} - Rating: {card2.rating} ({card2.wins}-{card2.losses})"
        ]

    def generate_tournament_report(self) -> dict:
        total_rating = sum(c.rating for c in self.cards.values())
        avg = int(total_rating / len(self.cards)) if self.cards else 0
        
        return {
            'total_cards': len(self.cards),
            'matches_played': self.matches_played,
            'avg_rating': avg,
            'platform_status': 'active'
        }
