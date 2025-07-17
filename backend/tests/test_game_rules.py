import pytest
from app.models.card import Card
from app.services.rules_engine import RulesEngine

class TestGameRules:
    def test_valid_straight_flush(self):
        """Test valid straight flush validation"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="5", suit="♠"),
            Card(rank="6", suit="♠"),
            Card(rank="7", suit="♠"),
        ]
        assert RulesEngine.is_valid_straight_flush(cards) == True

    def test_invalid_straight_flush_wrong_suit(self):
        """Test invalid straight flush with mixed suits"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♥"),
            Card(rank="5", suit="♠"),
        ]
        assert RulesEngine.is_valid_straight_flush(cards) == False

    def test_invalid_straight_flush_not_consecutive(self):
        """Test invalid straight flush with non-consecutive ranks"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="5", suit="♠"),
            Card(rank="7", suit="♠"),
        ]
        assert RulesEngine.is_valid_straight_flush(cards) == False

    def test_valid_sestina(self):
        """Test valid 6-card straight flush (sestina)"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="5", suit="♠"),
            Card(rank="6", suit="♠"),
            Card(rank="7", suit="♠"),
            Card(rank="8", suit="♠"),
        ]
        assert RulesEngine.is_valid_sestina(cards) == True

    def test_valid_sestina_with_wild_at_end(self):
        """Test valid sestina with wild card at the end"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="5", suit="♠"),
            Card(rank="6", suit="♠"),
            Card(rank="7", suit="♠"),
            Card(rank="8", suit="♠"),
            Card(rank="Joker", suit=""),
        ]
        assert RulesEngine.is_valid_sestina(cards) == True

    def test_invalid_sestina_with_wild_in_middle(self):
        """Test invalid sestina with wild card in the middle"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="Joker", suit=""),
            Card(rank="6", suit="♠"),
            Card(rank="7", suit="♠"),
            Card(rank="8", suit="♠"),
        ]
        assert RulesEngine.is_valid_sestina(cards) == False

    def test_card_values(self):
        """Test card value calculation"""
        assert RulesEngine.get_card_value(Card(rank="3", suit="♠")) == 5
        assert RulesEngine.get_card_value(Card(rank="7", suit="♠")) == 10
        assert RulesEngine.get_card_value(Card(rank="A", suit="♠")) == 15
        assert RulesEngine.get_card_value(Card(rank="Joker", suit="")) == 25
        assert RulesEngine.get_card_value(Card(rank="2", suit="♠", is_pinella=True)) == 20

    def test_valid_meld_with_joker(self):
        """Test valid meld with joker"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="Joker", suit=""),
            Card(rank="6", suit="♠"),
        ]
        assert RulesEngine.is_valid_meld(cards) == True

    def test_invalid_consecutive_jokers(self):
        """Test invalid meld with consecutive jokers"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="Joker", suit=""),
            Card(rank="Joker", suit=""),
            Card(rank="6", suit="♠"),
        ]
        assert RulesEngine.is_valid_meld(cards) == False

    def test_valid_pinella_usage(self):
        """Test valid pinella usage"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="5", suit="♠"),
            Card(rank="2", suit="♠", is_pinella=True),
        ]
        assert RulesEngine.is_valid_meld(cards) == True

    def test_pinnacolone_detection(self):
        """Test Pinnacolone (A-K straight flush) detection"""
        cards = [
            Card(rank="A", suit="♠"),
            Card(rank="2", suit="♠"),
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="5", suit="♠"),
            Card(rank="6", suit="♠"),
            Card(rank="7", suit="♠"),
            Card(rank="8", suit="♠"),
            Card(rank="9", suit="♠"),
            Card(rank="10", suit="♠"),
            Card(rank="J", suit="♠"),
            Card(rank="Q", suit="♠"),
            Card(rank="K", suit="♠"),
        ]
        assert RulesEngine.is_pinnacolone(cards) == True

    def test_bronze_bonus_calculation(self):
        """Test bronze bonus for long clean straights"""
        cards = [
            Card(rank="3", suit="♠"),
            Card(rank="4", suit="♠"),
            Card(rank="5", suit="♠"),
            Card(rank="6", suit="♠"),
            Card(rank="7", suit="♠"),
            Card(rank="8", suit="♠"),
            Card(rank="9", suit="♠"),
        ]
        bonus = RulesEngine.calculate_bronze_bonus(cards)
        assert bonus == 2  # 7+ cards, x2 bonus

    def test_scoring_calculation(self):
        """Test complete scoring calculation"""
        player_melds = [
            [  # Sestina - clean
                Card(rank="3", suit="♠"),
                Card(rank="4", suit="♠"),
                Card(rank="5", suit="♠"),
                Card(rank="6", suit="♠"),
                Card(rank="7", suit="♠"),
                Card(rank="8", suit="♠"),
            ]
        ]
        player_hand = [
            Card(rank="9", suit="♠"),
            Card(rank="10", suit="♠"),
        ]
        
        score = RulesEngine.calculate_player_score(
            melds=player_melds,
            hand=player_hand,
            has_closed=True,
            closed_clean=True
        )
        
        # Base meld value: 6*10 = 60
        # Sestina bonus: 60 * 2 = 120
        # Hand penalty: 2*10 = 20
        # Closure bonus: 100
        # Expected: 120 - 20 + 100 = 200
        assert score == 200