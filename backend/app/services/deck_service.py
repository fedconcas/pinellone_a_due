import random
from typing import List
from ..models.card import Card, Suit, Rank, CardType

class DeckService:
    """Service for managing card decks in Pinellone"""
    
    @staticmethod
    def create_full_deck() -> List[Card]:
        """Create a complete Pinellone deck (2 French decks, 108 cards)"""
        cards = []
        
        # Create two complete decks
        for _ in range(2):
            # Normal cards (excluding red 2s)
            for suit in [Suit.SPADES, Suit.CLUBS]:  # Black suits only for 2s
                cards.append(Card(rank="2", suit=suit.value, card_type=CardType.PINELLA))
            
            for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.SPADES, Suit.CLUBS]:
                for rank in ["A", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                    cards.append(Card(rank=rank, suit=suit.value))
            
            # Jokers (2 per deck)
            for _ in range(2):
                cards.append(Card(rank="Joker", suit="", card_type=CardType.JOKER))
        
        return cards
    
    @staticmethod
    def shuffle_deck(cards: List[Card]) -> List[Card]:
        """Shuffle the deck"""
        shuffled = cards.copy()
        random.shuffle(shuffled)
        return shuffled
    
    @staticmethod
    def deal_cards(deck: List[Card], num_players: int = 2, cards_per_player: int = 15) -> tuple[List[Card], List[List[Card]]]:
        """Deal cards to players and return remaining deck"""
        if len(deck) < num_players * cards_per_player:
            raise ValueError("Not enough cards in deck")
        
        hands = []
        remaining_deck = deck.copy()
        
        for i in range(num_players):
            hand = remaining_deck[:cards_per_player]
            remaining_deck = remaining_deck[cards_per_player:]
            hands.append(hand)
        
        return remaining_deck, hands
    
    @staticmethod
    def create_new_game_deck() -> List[Card]:
        """Create and shuffle a new game deck"""
        deck = DeckService.create_full_deck()
        return DeckService.shuffle_deck(deck)