import React from 'react';
import { useGameStore } from '../store/gameStore';
import { Card } from './Card';
import { Card as CardType } from '../types/game.types';

interface PlayerHandProps {
  playerIndex: number;
  playerId?: string; // Add player ID for fetching actual cards
  selectedCards?: number[];
  onCardSelect?: (index: number) => void;
}

export const PlayerHand: React.FC<PlayerHandProps> = ({ playerIndex, playerId, selectedCards = [], onCardSelect }) => {
  const { game, meldCards } = useGameStore();
  // Using props for selectedCards state
  
  if (!game) return null;

  const player = game.players[playerIndex];
  const isCurrentPlayer = game.current_player_index === playerIndex;
  
  console.log('PlayerHand render:', {
    playerIndex,
    isCurrentPlayer,
    currentPlayerIndex: game.current_player_index,
    phase: game.phase,
    selectedCards,
    onCardSelect: !!onCardSelect
  });
  
  // Only show actual cards for current player, otherwise show card backs
  const handCards: CardType[] = isCurrentPlayer && player.hand 
    ? player.hand 
    : Array(player.hand_count).fill(0).map((_, i) => ({
        rank: '?',
        suit: '?',
        card_type: 'normal',
        is_wild: false,
        value: 0
      }));

  const handleCardClick = (index: number) => {
    if (!isCurrentPlayer) return;
    if (game.phase !== 'play') return; // Only allow selection during play phase
    
    console.log('Card clicked:', index, 'isCurrentPlayer:', isCurrentPlayer, 'phase:', game.phase);
    onCardSelect && onCardSelect(index);
  };

  // Meld functionality is now handled by GameControls

  return (
    <div className="bg-white rounded-lg p-4 shadow-lg">
      <h3 className="text-lg font-bold mb-2">
        {player.name} {isCurrentPlayer && "(Your Turn)"}
      </h3>
      
      <div className="flex flex-wrap gap-2 mb-4">
        {handCards.map((card, index) => (
          <div key={index} className="inline-block">
            <Card
              card={card}
              onClick={() => handleCardClick(index)}
              isSelected={selectedCards.includes(index)}
              isDraggable={isCurrentPlayer && game.phase === 'play'}
              playerIndex={playerIndex}
              cardIndex={index}
            />
          </div>
        ))}
      </div>
      
      {/* Meld functionality is now handled by GameControls */}
    </div>
  );
};