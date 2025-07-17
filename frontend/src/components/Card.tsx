import React from 'react';
import { Card as CardType } from '../types/game.types';
import { useDraggable } from '@dnd-kit/core';

interface CardProps {
  card: CardType;
  onClick?: () => void;
  isSelected?: boolean;
  isDraggable?: boolean;
  className?: string;
  dragId?: string;
  playerIndex?: number;
  cardIndex?: number;
}

export const Card: React.FC<CardProps> = ({ 
  card, 
  onClick, 
  isSelected = false, 
  isDraggable = false,
  className = '',
  dragId,
  playerIndex,
  cardIndex
}) => {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: dragId || `card-${playerIndex}-${cardIndex}`,
    disabled: !isDraggable,
  });

  const getSuitColor = (suit: string) => {
    if (suit === '?') return 'text-blue-600'; // Card back color
    return ['♥', '♦'].includes(suit) ? 'text-red-600' : 'text-black';
  };

  const getCardDisplay = () => {
    // Show card back for hidden cards
    if (card.rank === '?' || card.suit === '?') {
      return '🂠'; // Card back emoji
    }
    
    if (card.card_type === 'joker') return 'JOKER';
    if (card.card_type === 'pinella') return `2${card.suit}`;
    
    // Map rank names to display symbols
    const rankMap: { [key: string]: string } = {
      'A': 'A',
      'K': 'K',
      'Q': 'Q',
      'J': 'J',
      '10': '10',
      '9': '9',
      '8': '8',
      '7': '7',
      '6': '6',
      '5': '5',
      '4': '4',
      '3': '3'
    };
    
    const displayRank = rankMap[card.rank] || card.rank;
    return `${displayRank}${card.suit}`;
  };

  const style = {
    transform: transform ? `translate3d(${transform.x}px, ${transform.y}px, 0)` : undefined,
    opacity: isDragging ? 0.5 : 1,
  };

  const isHidden = card.rank === '?' || card.suit === '?';
  
  return (
    <div
      ref={setNodeRef}
      style={style}
      {...(!isHidden ? listeners : {})}
      {...(!isHidden ? attributes : {})}
      className={`
        w-16 h-24 rounded-lg shadow-md
        flex items-center justify-center font-bold
        transition-all duration-200
        ${card.card_type === 'joker' ? 'text-xs' : 'text-lg'}
        ${isHidden ? 'bg-blue-900 border-2 border-blue-700' : 'bg-white border-2'}
        ${getSuitColor(card.suit)}
        ${isSelected ? 'border-blue-500 ring-2 ring-blue-300' : (isHidden ? 'border-blue-700' : 'border-gray-300')}
        ${onClick && !isHidden ? 'hover:shadow-lg hover:scale-105' : ''}
        ${isDraggable && !isHidden ? 'cursor-grab active:cursor-grabbing' : (isHidden ? 'cursor-default' : 'cursor-pointer')}
        ${isDragging ? 'z-50' : ''}
        ${className}
      `}
      onClick={!isHidden ? onClick : undefined}
    >
      {getCardDisplay()}
    </div>
  );
};
