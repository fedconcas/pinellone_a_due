import pytest
from app.services.game_service import GameService
from app.models.game import GamePhase

class TestNewDrawingSystem:
    
    def setup_method(self):
        self.service = GameService()
        self.game = self.service.create_game(["Player 1", "Player 2"])
    
    def test_draw_from_deck_two_cards(self):
        """Test drawing 2 cards from deck"""
        initial_hand_size = len(self.game.current_player.hand)
        initial_deck_size = len(self.game.deck)
        
        success = self.service.draw_cards(self.game.id, 'deck')
        
        assert success is True
        assert len(self.game.current_player.hand) == initial_hand_size + 2
        assert len(self.game.deck) == initial_deck_size - 2
        assert self.game.phase == GamePhase.PLAY
    
    def test_draw_from_discard_with_sequence(self):
        """Test drawing from discard pile with sequence"""
        # Add some cards to discard pile
        self.game.discard_pile.extend([self.game.deck.pop() for _ in range(3)])
        initial_hand_size = len(self.game.current_player.hand)
        initial_deck_size = len(self.game.deck)
        initial_discard_size = len(self.game.discard_pile)
        
        success = self.service.draw_cards(self.game.id, 'discard', 1)
        
        assert success is True
        # Should get 1 from deck + 2 from discard (index 1 and 2)
        assert len(self.game.current_player.hand) == initial_hand_size + 3
        assert len(self.game.deck) == initial_deck_size - 1
        assert len(self.game.discard_pile) == initial_discard_size - 2
    
    def test_draw_preview_deck(self):
        """Test preview for deck drawing"""
        preview = self.service.get_draw_preview(self.game.id, 'deck')
        
        assert preview is not None
        assert preview['draw_type'] == 'deck'
        assert preview['total_cards'] == 2
        assert preview['valid'] is True
    
    def test_draw_preview_discard(self):
        """Test preview for discard drawing"""
        # Add cards to discard
        self.game.discard_pile.extend([self.game.deck.pop() for _ in range(3)])
        
        preview = self.service.get_draw_preview(self.game.id, 'discard', 1)
        
        assert preview is not None
        assert preview['draw_type'] == 'discard'
        assert preview['total_cards'] == 3  # 1 from deck + 2 from discard
        assert preview['valid'] is True
    
    def test_invalid_draw_type(self):
        """Test invalid draw type"""
        success = self.service.draw_cards(self.game.id, 'invalid')
        assert success is False
    
    def test_draw_not_in_draw_phase(self):
        """Test drawing when not in draw phase"""
        self.game.phase = GamePhase.PLAY
        
        success = self.service.draw_cards(self.game.id, 'deck')
        assert success is False
    
    def test_insufficient_deck_cards(self):
        """Test drawing when deck has insufficient cards"""
        # Remove most cards from deck
        self.game.deck = self.game.deck[:1]
        
        success = self.service.draw_cards(self.game.id, 'deck')
        assert success is False
    
    def test_invalid_discard_index(self):
        """Test invalid discard index"""
        success = self.service.draw_cards(self.game.id, 'discard', 999)
        assert success is False
    
    def test_empty_discard_pile(self):
        """Test drawing from empty discard pile"""
        self.game.discard_pile = []
        
        success = self.service.draw_cards(self.game.id, 'discard', 0)
        assert success is False
    
    def test_language_toggle_integration(self):
        """Test that game state includes all necessary info for language toggle"""
        game_state = self.service.get_game_state(self.game.id)
        
        assert game_state is not None
        assert 'phase' in game_state
        assert 'players' in game_state
        assert len(game_state['players']) == 2
        assert 'name' in game_state['players'][0]
        assert 'hand_count' in game_state['players'][0]