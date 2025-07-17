import React, { useState } from 'react';
import { useGameStore } from '../store/gameStore';
import { useLanguage } from '../contexts/LanguageContext';
import { DrawingSelectionModal } from './DrawingSelectionModal';

interface GameControlsProps {
  selectedCards: number[];
  setSelectedCards: (cards: number[]) => void;
  selectedMeld: number | null;
  setSelectedMeld: (meld: number | null) => void;
}

export const GameControls: React.FC<GameControlsProps> = ({
  selectedCards,
  setSelectedCards,
  selectedMeld,
  setSelectedMeld
}) => {
  const { game, drawCards, meldCards, attachCard, discardCard } = useGameStore();
  const { t } = useLanguage();
  const [showDrawingModal, setShowDrawingModal] = useState(false);

  if (!game) return null;

  const currentPlayer = game.players[game.current_player_index];
  const isCurrentPlayer = true; // This would be determined by actual player ID

  const handleDraw = async (drawType: 'deck' | 'discard', discardIndex?: number) => {
    try {
      await drawCards(game.id, drawType, discardIndex);
      setShowDrawingModal(false);
    } catch (error) {
      console.error('Failed to draw cards:', error);
    }
  };

  const handleMeld = async () => {
    if (selectedCards.length === 0) return;
    
    try {
      await meldCards(game.id, selectedCards);
      setSelectedCards([]);
    } catch (error) {
      console.error('Failed to meld cards:', error);
    }
  };

  const handleAttach = async () => {
    if (selectedCards.length !== 1 || selectedMeld === null) return;
    
    try {
      await attachCard(game.id, selectedCards[0], selectedMeld);
      setSelectedCards([]);
      setSelectedMeld(null);
    } catch (error) {
      console.error('Failed to attach card:', error);
    }
  };

    const handleDiscard = async (cardIndex: number) => {
      try {
        await discardCard(game.id, cardIndex);
        // End turn logic goes here if needed
      } catch (error) {
        console.error('Failed to discard card:', error);
      }
    };

  // Card selection is now handled by parent component

  return (
    <div className="bg-white rounded-lg p-4 shadow-lg">
      <h3 className="text-lg font-bold mb-4">{t('game.controls')}</h3>
      
      <div className="space-y-3">
        {/* Draw Phase */}
        {game.phase === 'draw' && isCurrentPlayer && (
          <button
            onClick={() => setShowDrawingModal(true)}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
          >
            {t('game.drawCards')}
          </button>
        )}

        {/* Play Phase - Show meld controls and discard instructions */}
        {game.phase === 'play' && isCurrentPlayer && (
          <>
            <div className="border-t pt-3">
              <h4 className="font-medium mb-2">{t('game.selectedCards')}: {selectedCards.length}</h4>
              
              <button
                onClick={handleMeld}
                disabled={selectedCards.length < 3}
                className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed mb-2"
              >
                {t('game.meld')} ({selectedCards.length}/3+ cards)
              </button>
              
              <button
                onClick={handleAttach}
                disabled={selectedCards.length !== 1 || selectedMeld === null}
                className="w-full bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 disabled:opacity-50 disabled:cursor-not-allowed mb-2"
              >
                {t('game.attach')}
              </button>
            </div>
            
            <div className="border-t pt-3">
              <h4 className="font-medium mb-2">{t('game.endTurn')}</h4>
              <div className="text-sm text-gray-600 space-y-1">
                <p>• {t('game.dragToDiscard')}</p>
                <p>• {t('game.discardEndsTheTurn')}</p>
              </div>
            </div>
          </>
        )}

        {/* Game Info */}
        <div className="border-t pt-3 text-sm">
          <div><strong>{t('game.phase')}:</strong> {t(`game.phase.${game.phase}`)}</div>
          <div><strong>{t('game.currentPlayer')}:</strong> {currentPlayer.name}</div>
          <div><strong>{t('game.cardsInHand')}:</strong> {currentPlayer.hand_count}</div>
        </div>

        {/* Rules Display */}
        <div className="border-t pt-3">
          <h4 className="font-medium mb-2">{t('game.rules')}</h4>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• {t('rules.drawTwo')}</li>
            <li>• {t('rules.discardSequence')}</li>
            <li>• {t('rules.meldThree')}</li>
          </ul>
        </div>
      </div>

      <DrawingSelectionModal
        isOpen={showDrawingModal}
        onClose={() => setShowDrawingModal(false)}
        onDraw={handleDraw}
      />
    </div>
  );
};