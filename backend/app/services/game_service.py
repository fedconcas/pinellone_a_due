import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from ..models.game import GameState, GamePhase
from ..models.player import PlayerState
from ..models.card import Card
from .deck_service import DeckService
from .rules_engine import RulesEngine

class GameService:
    """Main service for managing Pinellone game logic"""
    
    def __init__(self):
        self.games: Dict[str, GameState] = {}
    
    def create_game(self, player_names: List[str]) -> GameState:
        """Create a new game with two players"""
        if len(player_names) != 2:
            raise ValueError("Exactly 2 players required")
        
        game_id = str(uuid.uuid4())
        
        # Create and shuffle deck
        deck = DeckService.create_new_game_deck()
        
        # Deal cards
        remaining_deck, hands = DeckService.deal_cards(deck, 2, 15)
        
        # Create players
        players = [
            PlayerState(
                id=str(uuid.uuid4()),
                name=player_names[0],
                hand=hands[0]
            ),
            PlayerState(
                id=str(uuid.uuid4()),
                name=player_names[1],
                hand=hands[1]
            )
        ]
        
        # Create initial empty discard pile
        discard_pile = []
        
        game = GameState(
            id=game_id,
            players=players,
            deck=remaining_deck,
            discard_pile=discard_pile
        )
        
        self.games[game_id] = game
        return game
    
    def get_game(self, game_id: str) -> Optional[GameState]:
        """Get a game by ID"""
        return self.games.get(game_id)
    
    def draw_cards(self, game_id: str, draw_type: str, discard_index: Optional[int] = None) -> bool:
        """Flexible drawing system supporting new Pinellone rules:
        - 'deck': Draw 2 cards from deck
        - Starting the game ensures the first player draws 2 cards from the deck when the discard pile is empty
        - 'discard': Draw 1 from deck + cards from discard (target + all above)
        """
        game = self.get_game(game_id)
        if not game:
            return False
        
        if game.phase != GamePhase.DRAW:
            return False
        
        if draw_type == 'deck':
            # Draw 2 cards from deck
            if len(game.deck) < 2:
                return False
            
            cards_drawn = []
            for _ in range(2):
                card = game.deck.pop()
                game.current_player.add_card(card)
                cards_drawn.append(card)
            
        elif draw_type == 'discard':
            # Check if discard pile is empty (first turn rule)
            if not game.discard_pile:
                return False
            
            # Validate discard index
            if discard_index is None or discard_index >= len(game.discard_pile):
                return False
            
            # Must have at least 1 card in deck
            if not game.deck:
                return False
            
            # Draw 1 from deck
            deck_card = game.deck.pop()
            game.current_player.add_card(deck_card)
            
            # Take target card and all above from discard
            cards_to_take = game.discard_pile[discard_index:]
            game.discard_pile = game.discard_pile[:discard_index]
            
            for card in cards_to_take:
                game.current_player.add_card(card)
                
        else:
            return False
        
        game.phase = GamePhase.PLAY
        game.updated_at = datetime.now()
        
        return True
    
    def get_draw_preview(self, game_id: str, draw_type: str, discard_index: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Preview what cards would be drawn without actually drawing them"""
        game = self.get_game(game_id)
        if not game:
            return None
        
        if game.phase != GamePhase.DRAW:
            return None
        
        preview = {
            "draw_type": draw_type,
            "cards_to_draw": [],
            "total_cards": 0,
            "valid": False
        }
        
        if draw_type == 'deck':
            if len(game.deck) >= 2:
                # Preview 2 cards from deck (without revealing them)
                preview["cards_to_draw"] = ["deck_card_1", "deck_card_2"]
                preview["total_cards"] = 2
                preview["valid"] = True
                
        elif draw_type == 'discard':
            if discard_index is not None and discard_index < len(game.discard_pile):
                # Preview 1 from deck + discard cards
                discard_cards = game.discard_pile[discard_index:]
                preview["cards_to_draw"] = ["deck_card"] + [str(card) for card in discard_cards]
                preview["total_cards"] = 1 + len(discard_cards)
                preview["valid"] = True
        
        return preview
    
    def meld_cards(self, game_id: str, card_indices: List[int]) -> bool:
        """Meld cards from player's hand"""
        game = self.get_game(game_id)
        if not game:
            return False
        
        if game.phase != GamePhase.PLAY:
            return False
        
        player = game.current_player
        
        # Validate indices
        if any(i < 0 or i >= len(player.hand) for i in card_indices):
            return False
        
        # Get cards to meld
        cards_to_meld = [player.hand[i] for i in card_indices]
        
        # Validate meld
        if not RulesEngine.can_meld(cards_to_meld, player.has_opened):
            return False
        
        # Remove cards from hand and add to melds
        for i in sorted(card_indices, reverse=True):
            player.hand.pop(i)
        
        player.add_meld(cards_to_meld)
        game.updated_at = datetime.now()
        
        return True
    
    def attach_card(self, game_id: str, card_index: int, meld_index: int) -> bool:
        """Attach a card to an existing meld"""
        game = self.get_game(game_id)
        if not game:
            return False
        
        if game.phase != GamePhase.PLAY:
            return False
        
        player = game.current_player
        
        # Validate indices
        if card_index < 0 or card_index >= len(player.hand):
            return False
        
        if meld_index < 0 or meld_index >= len(player.melds):
            return False
        
        card = player.hand[card_index]
        target_meld = player.melds[meld_index]
        
        # Validate attachment
        if not RulesEngine.can_attach(card, target_meld):
            return False
        
        # Remove card from hand and add to meld
        player.hand.pop(card_index)
        target_meld.append(card)
        target_meld.sort(key=lambda c: c.sort_key)
        
        game.updated_at = datetime.now()
        
        return True
    
    def discard_card(self, game_id: str, card_index: int) -> bool:
        """Discard a card and end turn"""
        game = self.get_game(game_id)
        if not game:
            return False
        
        if game.phase != GamePhase.PLAY:
            return False
        
        player = game.current_player
        
        # Validate index
        if card_index < 0 or card_index >= len(player.hand):
            return False
        
        # Player must have opened to discard
        if not player.has_opened:
            return False
        
        # Discard card
        card = player.hand.pop(card_index)
        game.discard_pile.append(card)
        
        # Advance turn
        game.advance_turn()
        
        return True
    
    def close_game(self, game_id: str) -> bool:
        """Attempt to close the game"""
        game = self.get_game(game_id)
        if not game:
            return False
        
        player = game.current_player
        
        # Must have exactly 1 card in hand
        if len(player.hand) != 1:
            return False
        
        # Must have a sestina
        if not player.has_sestina():
            return False
        
        # Discard final card
        final_card = player.hand.pop()
        game.discard_pile.append(final_card)
        
        # Calculate final scores
        scores = game.get_scores()
        for player in game.players:
            player.score = scores[player.id]
        
        return True
    
    def get_game_state(self, game_id: str, player_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get complete game state for API
        
        Args:
            game_id: The game ID
            player_id: Optional player ID to expose hand details to owning player
        """
        game = self.get_game(game_id)
        if not game:
            return None
        
        def format_player_state(player: PlayerState, is_owning_player: bool = False) -> Dict[str, Any]:
            """Format player state with appropriate visibility"""
            if is_owning_player:
                # Expose actual cards to owning player
                return {
                    "id": player.id,
                    "name": player.name,
                    "hand": [card.dict() for card in player.hand],
                    "hand_count": len(player.hand),
                    "melds": [[card.dict() for card in meld] for meld in player.melds],
                    "has_opened": player.has_opened,
                    "score": player.score,
                    "can_close": player.can_close()
                }
            else:
                # Hide cards from other players
                return {
                    "id": player.id,
                    "name": player.name,
                    "hand_count": len(player.hand),
                    "melds": [[str(c) for c in meld] for meld in player.melds],
                    "has_opened": player.has_opened,
                    "score": player.score,
                    "can_close": player.can_close()
                }
        
        return {
            "id": game.id,
            "players": [
                format_player_state(player, player.id == player_id)
                for player in game.players
            ],
            "current_player_index": game.current_player_index,
            "phase": game.phase,
            "deck_count": len(game.deck),
            "discard_pile": [card.dict() for card in game.discard_pile],
            "is_game_over": game.is_game_over()
        }