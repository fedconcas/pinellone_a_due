from enum import Enum
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from .card import Card
from .player import PlayerState

class GamePhase(str, Enum):
    DRAW = "draw"
    PLAY = "play"
    DISCARD = "discard"

class GameState(BaseModel):
    id: str
    players: List[PlayerState] = Field(default_factory=list)
    deck: List[Card] = Field(default_factory=list)
    discard_pile: List[Card] = Field(default_factory=list)
    current_player_index: int = 0
    phase: GamePhase = GamePhase.DRAW
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def current_player(self) -> PlayerState:
        """Get the current player"""
        return self.players[self.current_player_index]
    
    @property
    def next_player_index(self) -> int:
        """Get the index of the next player"""
        return (self.current_player_index + 1) % len(self.players)
    
    @property
    def next_player(self) -> PlayerState:
        """Get the next player"""
        return self.players[self.next_player_index]
    
    def advance_turn(self) -> None:
        """Move to the next player's turn"""
        self.current_player_index = self.next_player_index
        self.phase = GamePhase.DRAW
        self.updated_at = datetime.now()
    
    def is_game_over(self) -> bool:
        """Check if the game has ended"""
        return any(player.can_close() for player in self.players)
    
    def get_winner(self) -> Optional[PlayerState]:
        """Get the winning player if game is over"""
        if not self.is_game_over():
            return None
        
        # Player who closed wins
        for player in self.players:
            if player.can_close():
                return player
        
        return None
    
    def get_scores(self) -> Dict[str, int]:
        """Calculate final scores for all players"""
        scores = {}
        
        for player in self.players:
            if player.can_close():
                # Player who closed gets bonus
                scores[player.id] = player.score + 100
            else:
                # Other players get penalty for cards in hand
                scores[player.id] = player.score - player.get_hand_value()
        
        return scores
    
    def __str__(self) -> str:
        return f"Game {self.id} - Player {self.current_player_index}'s turn"