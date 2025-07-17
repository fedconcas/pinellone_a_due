"""
Comprehensive test suite for Pinellone a 15 carte rules validation
"""
import pytest
from app.services.deck_service import DeckService
from app.services.rules_engine import RulesEngine
from app.services.game_service import GameService
from app.models.card import Card, CardType, Suit, Rank

class TestPinelloneRules:
    
    def test_deck_composition(self):
        """Test that deck has correct composition: 2x54 cards, no red 2s, with jolly/pinelle"""
        deck = DeckService.create_new_game_deck()
        
        # Should have 108 cards (2x54)
        assert len(deck) == 108
        
        # Count card types
        jokers = [c for c in deck if c.card_type == CardType.JOKER]
        pinelle = [c for c in deck if c.is_pinella]
        normal_cards = [c for c in deck if c.card_type == CardType.NORMAL]
        
        # Should have 4 jokers (2 per deck)
        assert len(jokers) == 4
        
        # Should have 2 pinelle (1 per deck)
        assert len(pinelle) == 2
        
        # Should have no red 2s (hearts or diamonds)
        red_2s = [c for c in deck if c.rank == '2' and c.suit in [Suit.HEARTS, Suit.DIAMONDS]]
        assert len(red_2s) == 0
        
        # Should have black 2s as pinelle
        black_2s = [c for c in deck if c.rank == '2' and c.suit in [Suit.SPADES, Suit.CLUBS]]
        assert len(black_2s) == 2
    
    def test_initial_deal(self):
        """Test that each player gets exactly 15 cards"""
        game_service = GameService()
        game = game_service.create_game(["Player1", "Player2"])
        
        assert len(game.players[0].hand) == 15
        assert len(game.players[1].hand) == 15
    
    def test_draw_rules(self):
        """Test that players draw 2 cards per turn"""
        game_service = GameService()
        game = game_service.create_game(["Player1", "Player2"])
        
        initial_count = len(game.players[0].hand)
        
        # Draw from deck should give 2 cards
        game_service.draw_from_deck(game.id)
        assert len(game.players[0].hand) == initial_count + 2
    
    def test_scale_validation(self):
        """Test that only sequences of 3+ same-suit consecutive cards are valid"""
        # Valid scale: 3♠, 4♠, 5♠
        valid_scale = [
            Card(rank='3', suit='♠'),
            Card(rank='4', suit='♠'),
            Card(rank='5', suit='♠')
        ]
        assert RulesEngine.is_valid_scale(valid_scale)
        
        # Invalid: wrong suit
        invalid_suit = [
            Card(rank='3', suit='♠'),
            Card(rank='4', suit='♥'),
            Card(rank='5', suit='♠')
        ]
        assert not RulesEngine.is_valid_scale(invalid_suit)
        
        # Invalid: not consecutive
        invalid_sequence = [
            Card(rank='3', suit='♠'),
            Card(rank='5', suit='♠'),
            Card(rank='7', suit='♠')
        ]
        assert not RulesEngine.is_valid_scale(invalid_sequence)
    
    def test_wild_card_placement(self):
        """Test that jolly/pinelle cannot be consecutive in scales"""
        # Valid: wild cards not consecutive
        valid_with_wild = [
            Card(rank='3', suit='♠'),
            Card(rank='4', suit='♠'),
            Card(rank='5', suit='♠', card_type=CardType.PINELLA),
            Card(rank='7', suit='♠')
        ]
        assert RulesEngine.is_valid_scale(valid_with_wild)
        
        # Invalid: consecutive wild cards
        invalid_consecutive = [
            Card(rank='3', suit='♠'),
            Card(rank='4', suit='♠', card_type=CardType.PINELLA),
            Card(rank='5', suit='♠', card_type=CardType.JOKER),
            Card(rank='6', suit='♠')
        ]
        assert not RulesEngine.is_valid_scale(invalid_consecutive)
    
    def test_sestina_requirement(self):
        """Test that 6+ card sequence is required for closing"""
        # Valid sestina: 6 consecutive cards
        valid_sestina = [
            Card(rank='3', suit='♠'),
            Card(rank='4', suit='♠'),
            Card(rank='5', suit='♠'),
            Card(rank='6', suit='♠'),
            Card(rank='7', suit='♠'),
            Card(rank='8', suit='♠')
        ]
        assert RulesEngine.is_valid_sestina(valid_sestina)
        
        # Invalid: less than 6 cards
        invalid_length = [
            Card(rank='3', suit='♠'),
            Card(rank='4', suit='♠'),
            Card(rank='5', suit='♠')
        ]
        assert not RulesEngine.is_valid_sestina(invalid_length)
    
    def test_pinnacolone_detection(self):
        """Test detection of pinnacolone (A-K-A straight flush)"""
        # Valid pinnacolone: A,2,3,4,5,6,7,8,9,10,J,Q,K,A
        pinnacolone = [
            Card(rank='A', suit='♠'),
            Card(rank='2', suit='♠', card_type=CardType.PINELLA),
            Card(rank='3', suit='♠'),
            Card(rank='4', suit='♠'),
            Card(rank='5', suit='♠'),
            Card(rank='6', suit='♠'),
            Card(rank='7', suit='♠'),
            Card(rank='8', suit='♠'),
            Card(rank='9', suit='♠'),
            Card(rank='10', suit='♠'),
            Card(rank='J', suit='♠'),
            Card(rank='Q', suit='♠'),
            Card(rank='K', suit='♠'),
            Card(rank='A', suit='♠')
        ]
        assert RulesEngine.is_pinnacolone(pinnacolone)
    
    def test_card_values(self):
        """Test correct card values for scoring"""
        # Test normal cards
        card_3 = Card(rank='3', suit='♠')
        assert card_3.value == 5
        
        card_10 = Card(rank='10', suit='♠')
        assert card_10.value == 10
        
        card_A = Card(rank='A', suit='♠')
        assert card_A.value == 15
        
        # Test wild cards
        pinella = Card(rank='2', suit='♠', card_type=CardType.PINELLA)
        assert pinella.value == 20
        
        joker = Card(rank='JOKER', suit='JOKER', card_type=CardType.JOKER)
        assert joker.value == 25

if __name__ == "__main__":
    pytest.main([__file__])