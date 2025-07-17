from enum import Enum
from typing import List, Dict, Tuple
from pydantic import BaseModel

class Suit(str, Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

class Rank(str, Enum):
    ACE = "A"
    # Note: 2s are removed except as pinelle
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

class CardType(str, Enum):
    NORMAL = "normal"
    JOKER = "joker"
    PINELLA = "pinella"

class Card(BaseModel):
    rank: str
    suit: str
    card_type: CardType = CardType.NORMAL
    
    @property
    def is_joker(self) -> bool:
        return self.card_type == CardType.JOKER
    
    @property
    def is_pinella(self) -> bool:
        return self.card_type == CardType.PINELLA
    
    @property
    def is_wild(self) -> bool:
        return self.is_joker or self.is_pinella
    
    @property
    def value(self) -> int:
        """Card value for scoring"""
        if self.is_joker:
            return 25
        if self.is_pinella:
            return 20
        if self.rank == Rank.ACE:
            return 15
        if self.rank in [Rank.TEN.value, Rank.JACK.value, Rank.QUEEN.value, Rank.KING.value]:
            return 10
        if self.rank in [Rank.SIX.value, Rank.SEVEN.value, Rank.EIGHT.value, Rank.NINE.value]:
            return 10
        if self.rank in [Rank.THREE.value, Rank.FOUR.value, Rank.FIVE.value]:
            return 5
        return 0
    
    @property
    def sort_key(self) -> Tuple[int, int]:
        """For sorting cards by suit then rank"""
        rank_order = {
            Rank.ACE.value: 1, Rank.THREE.value: 3, Rank.FOUR.value: 4, Rank.FIVE.value: 5,
            Rank.SIX.value: 6, Rank.SEVEN.value: 7, Rank.EIGHT.value: 8, Rank.NINE.value: 9,
            Rank.TEN.value: 10, Rank.JACK.value: 11, Rank.QUEEN.value: 12, Rank.KING.value: 13
        }
        suit_order = {Suit.SPADES.value: 1, Suit.HEARTS.value: 2, Suit.DIAMONDS.value: 3, Suit.CLUBS.value: 4}
        
        if self.is_wild:
            return (99, 99)  # Wild cards at the end
        
        return (suit_order.get(self.suit, 0), rank_order.get(self.rank, 0))
    
    def __str__(self) -> str:
        if self.is_joker:
            return "Joker"
        if self.is_pinella:
            return f"2{self.suit}"
        return f"{self.rank}{self.suit}"
    
    def __hash__(self):
        return hash((self.rank, self.suit, self.card_type))
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return (self.rank, self.suit, self.card_type) == (other.rank, other.suit, other.card_type)