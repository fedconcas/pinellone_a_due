import React from 'react';
import { useGameStore } from '../store/gameStore';
import { Card } from './Card';
import { useDroppable } from '@dnd-kit/core';

export const MeldsDisplay: React.FC = () => {
  const { game } = useGameStore();
  
  if (!game) return null;

  const handleDrop = (playerIndex, meldIndex) => (event) => {
    const cardId = event.active.id;
    // Add logic to place the card onto the meld
  };

  return (
    <div className="bg-white rounded-lg p-4 shadow-lg">
      <h3 className="text-lg font-bold mb-4">Melds on Table</h3>
      
      <div className="space-y-4">
        {game.players.map((player, playerIndex) => (
          <div key={player.id} className="border rounded-lg p-3">
            <h4 className="font-semibold mb-2">{player.name}'s Melds</h4>
            
            {player.melds.length === 0 ? (
              <p className="text-sm text-gray-500">No melds yet</p>
            ) : (
              <div className="space-y-2">
                {player.melds.map((meld, meldIndex) => {
                  const { setNodeRef, isOver } = useDroppable({
                    id: `meld-${playerIndex}-${meldIndex}`
                  });
                  return (
                    <div 
                      key={meldIndex} 
                      ref={setNodeRef} 
                      className={`flex gap-1 ${isOver ? 'border-2 border-blue-500' : ''}`} 
                      onDrop={handleDrop(playerIndex, meldIndex)}
                    >
                      {meld.map((card, cardIndex) => (
                        <Card key={cardIndex} card={card} className="w-12 h-16 text-sm" />
                      ))}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};