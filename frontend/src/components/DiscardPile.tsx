import React from 'react';
import { useGameStore } from '../store/gameStore';
import { Card } from './Card';
import { useDroppable } from '@dnd-kit/core';

export const DiscardPile: React.FC = () => {
  const { game, drawCards } = useGameStore();
  const { isOver, setNodeRef } = useDroppable({
    id: 'discard-pile',
  });
  
  if (!game) return null;

  const handleDrawFromDiscard = async (cardIndex: number) => {
    try {
      await drawCards(game.id, 'discard', cardIndex);
    } catch (error) {
      console.error('Failed to draw from discard:', error);
    }
  };

  return (
    <div className="bg-white rounded-lg p-4 shadow-lg">
      <h3 className="text-lg font-bold mb-4">Discard Pile</h3>
      
      <div 
        ref={setNodeRef}
        className={`flex flex-col items-center transition-all duration-200 ${
          isOver ? 'bg-red-50 border-2 border-red-300 border-dashed' : ''
        }`}
      >
        {game.discard_pile.length === 0 ? (
          <div className="w-16 h-24 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
            <span className="text-gray-400 text-sm">Empty</span>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="text-sm text-gray-600 mb-2">
              {game.discard_pile.length} cards
            </div>
            
            {/* Show top 3 cards */}
            <div className="flex gap-2">
              {game.discard_pile.slice(-3).map((card, index) => (
                <div key={index} className="relative">
                  <Card 
                    card={card} 
                    className="w-16 h-24"
                    onClick={() => game.phase === 'draw' && handleDrawFromDiscard(game.discard_pile.length - 3 + index)}
                  />
                  {game.phase === 'draw' && (
                    <div className="absolute inset-0 bg-black bg-opacity-20 rounded-lg flex items-center justify-center">
                      <span className="text-white text-xs">Draw</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
        
        {isOver && (
          <div className="absolute inset-0 bg-red-100 bg-opacity-75 rounded-lg flex items-center justify-center">
            <span className="text-red-700 font-bold">Drop to Discard</span>
          </div>
        )}
      </div>
    </div>
  );
};