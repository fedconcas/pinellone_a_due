from typing import List, Optional, Tuple
from ..models.card import Card, CardType

class RulesEngine:
    """Engine for validating game rules and moves according to Pinellone a 15 carte rules"""
    
    @staticmethod
    def is_valid_scale(cards: List[Card]) -> bool:
        """Check if cards form a valid scale (straight flush of 3+ consecutive cards)"""
        if len(cards) < 3:
            return False
        
        # All non-wild cards must be same suit
        suit = None
        non_wild_cards = [card for card in cards if not card.is_wild]
        
        if not non_wild_cards:
            return False  # Cannot have all wild cards
        
        # Check suit consistency
        suit = non_wild_cards[0].suit
        for card in non_wild_cards:
            if card.suit != suit:
                return False
        
        # Get rank values for sorting (A=1, 3-K=3-13)
        def get_rank_value(rank: str) -> int:
            rank_map = {
                "A": 1, "3": 3, "4": 4, "5": 5,
                "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                "J": 11, "Q": 12, "K": 13
            }
            return rank_map.get(rank, 0)
        
        # Sort non-wild cards by rank
        sorted_non_wild = sorted(non_wild_cards, key=lambda c: get_rank_value(c.rank))
        
        # Check for consecutive sequence in non-wild cards
        if len(sorted_non_wild) > 1:
            for i in range(len(sorted_non_wild) - 1):
                current_rank = get_rank_value(sorted_non_wild[i].rank)
                next_rank = get_rank_value(sorted_non_wild[i + 1].rank)
                if next_rank - current_rank != 1:
                    return False
        
        # Check wild card positioning - no consecutive wilds allowed
        wild_positions = [i for i, card in enumerate(cards) if card.is_wild]
        for i in range(len(wild_positions) - 1):
            if wild_positions[i + 1] - wild_positions[i] == 1:
                return False  # Consecutive wild cards not allowed
        
        return True
    
    @staticmethod
    def is_valid_sestina(cards: List[Card]) -> bool:
        """Check if cards form a valid sestina (6+ card straight, wilds only at ends)"""
        if len(cards) < 6:
            return False
        
        # Filter out wild cards to check the core sequence
        non_wild_cards = [card for card in cards if not card.is_wild]
        
        # Must have at least 6 non-wild cards for a valid sestina
        if len(non_wild_cards) < 6:
            return False
        
        # Check if non-wild cards form a valid scale
        if not RulesEngine.is_valid_scale(non_wild_cards):
            return False
        
        # Wild cards can only be at the beginning or end
        wild_positions = [i for i, card in enumerate(cards) if card.is_wild]
        non_wild_positions = [i for i, card in enumerate(cards) if not card.is_wild]
        
        # All wild cards must be at the beginning or end
        if wild_positions:
            # Check if wild cards are only at start or end
            first_non_wild = min(non_wild_positions)
            last_non_wild = max(non_wild_positions)
            
            # Wild cards must be before first non-wild or after last non-wild
            for pos in wild_positions:
                if pos > first_non_wild and pos < last_non_wild:
                    return False
        
        return True
    
    @staticmethod
    def can_meld(cards: List[Card], player_has_opened: bool) -> bool:
        """Check if player can meld these cards"""
        if not player_has_opened:
            # First meld must be a sestina
            return RulesEngine.is_valid_sestina(cards)
        
        # Subsequent melds can be any valid scale
        return RulesEngine.is_valid_scale(cards)
    
    @staticmethod
    def can_attach(card: Card, target_meld: List[Card]) -> bool:
        """Check if a card can be attached to an existing meld"""
        if not target_meld:
            return False
        
        # Create temporary meld with the new card
        temp_meld = target_meld + [card]
        return RulesEngine.is_valid_scale(temp_meld)
    
    @staticmethod
    def get_meld_value(meld: List[Card]) -> int:
        """Calculate the value of a meld for scoring"""
        base_value = sum(card.value for card in meld)
        
        # Bonus for clean sestina (no wilds)
        if RulesEngine.is_valid_sestina(meld):
            return base_value * 2
        
        # Bonus for long scales
        if len(meld) >= 10 and not any(card.is_wild for card in meld):
            return base_value * 3
        elif len(meld) >= 7 and not any(card.is_wild for card in meld):
            return base_value * 2
        
        return base_value
    
    @staticmethod
    def is_pinnacolone(meld: List[Card]) -> bool:
        """Check if meld is a pinnacolone (A-K straight, 13 cards)"""
        if len(meld) != 13:
            return False
        
        # No wild cards
        if any(card.is_wild for card in meld):
            return False
        
        # All same suit
        suit = meld[0].suit
        if not all(card.suit == suit for card in meld):
            return False
        
        # Must contain all ranks A-K (including 2s as pinelle)
        required_ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
        meld_ranks = {card.rank for card in meld}
        
        return required_ranks == meld_ranks