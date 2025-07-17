from typing import List, Optional
from pydantic import BaseModel
from .card import Card

class PlayerState(BaseModel):
    id: str
    name: str
    hand: List[Card] = []
    melds: List[List[Card]] = []  # Each meld is a list of cards
    has_opened: bool = False  # Has player made their first meld?
    score: int = 0
    
    def add_card(self, card: Card) -> None:
        """Add a card to player's hand"""
        self.hand.append(card)
        self.hand.sort(key=lambda c: c.sort_key)
    
    def remove_card(self, card: Card) -> bool:
        """Remove a card from player's hand"""
        try:
            self.hand.remove(card)
            return True
        except ValueError:
            return False
    
    def remove_cards(self, cards: List[Card]) -> bool:
        """Remove multiple cards from hand"""
        for card in cards:
            if not self.remove_card(card):
                return False
        return True
    
    def add_meld(self, meld: List[Card]) -> None:
        """Add a new meld to player's melds"""
        self.melds.append(meld)
        if not self.has_opened:
            self.has_opened = True
    
    def get_hand_value(self) -> int:
        """Calculate total value of cards in hand"""
        return sum(card.value for card in self.hand)
    
    def has_sestina(self) -> bool:
        """Check if player has at least one 6-card straight"""
        from ..services.rules_engine import RulesEngine
        return any(
            RulesEngine.is_valid_sestina(meld) 
            for meld in self.melds
        )
    
    def can_close(self) -> bool:
        """Check if player can close the game"""
        return self.has_sestina() and len(self.hand) == 1
    
    def __str__(self) -> str:
        return f"Player {self.name} (ID: {self.id})"