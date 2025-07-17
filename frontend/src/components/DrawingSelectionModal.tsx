import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { useGameStore } from '../store/gameStore';
import { Card } from './Card';

interface DrawingSelectionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDraw: (drawType: 'deck' | 'discard', discardIndex?: number) => void;
}

export const DrawingSelectionModal: React.FC<DrawingSelectionModalProps> = ({
  isOpen,
  onClose,
  onDraw
}) => {
  const { t } = useLanguage();
  const { game } = useGameStore();
  const [selectedDrawType, setSelectedDrawType] = useState<'deck' | 'discard' | null>(null);
  const [selectedDiscardIndex, setSelectedDiscardIndex] = useState<number | null>(null);
  const [preview, setPreview] = useState<any>(null);

  useEffect(() => {
    if (selectedDrawType === 'discard' && selectedDiscardIndex !== null) {
      // Get preview from backend
      fetchDrawPreview();
    }
  }, [selectedDrawType, selectedDiscardIndex]);

  const fetchDrawPreview = async () => {
    if (!game) return;
    
    try {
      const response = await fetch(`http://localhost:8000/games/${game.id}/draw-preview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          game_id: game.id,
          draw_type: 'discard',
          card_index: selectedDiscardIndex
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setPreview(data);
      }
    } catch (error) {
      console.error('Error fetching draw preview:', error);
    }
  };

  const handleDraw = () => {
    if (selectedDrawType === 'deck') {
      onDraw('deck');
    } else if (selectedDrawType === 'discard' && selectedDiscardIndex !== null) {
      onDraw('discard', selectedDiscardIndex);
    }
    resetSelection();
  };

  const resetSelection = () => {
    setSelectedDrawType(null);
    setSelectedDiscardIndex(null);
    setPreview(null);
  };

  const handleClose = () => {
    resetSelection();
    onClose();
  };

  if (!isOpen || !game) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">{t('draw.title')}</h2>
          <button
            onClick={handleClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Deck Option */}
          <div
            className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
              selectedDrawType === 'deck'
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onClick={() => {
              setSelectedDrawType('deck');
              setSelectedDiscardIndex(null);
              setPreview({ total_cards: 2, cards_to_draw: ['deck_card_1', 'deck_card_2'] });
            }}
          >
            <h3 className="text-lg font-semibold mb-2">{t('draw.deck')}</h3>
            <p className="text-sm text-gray-600 mb-2">{t('draw.deckDescription')}</p>
            <div className="text-sm font-medium text-blue-600">
              {t('draw.cardsToDraw', { count: 2 })}
            </div>
          </div>

          {/* Discard Option */}
          <div
            className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
              selectedDrawType === 'discard'
                ? 'border-green-500 bg-green-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onClick={() => {
              setSelectedDrawType('discard');
              setSelectedDiscardIndex(null);
            }}
          >
            <h3 className="text-lg font-semibold mb-2">{t('draw.discard')}</h3>
            <p className="text-sm text-gray-600 mb-2">{t('draw.discardDescription')}</p>
            {selectedDrawType === 'discard' && (
              <div className="text-sm font-medium text-green-600">
                {preview && t('draw.cardsToDraw', { count: preview.total_cards })}
              </div>
            )}
          </div>
        </div>

        {/* Discard Pile Selection */}
        {selectedDrawType === 'discard' && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-3">{t('draw.selectCard')}</h3>
            {game.discard_pile && game.discard_pile.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {game.discard_pile.map((card, index) => (
                  <div
                    key={index}
                    className={`cursor-pointer transition-all ${
                      selectedDiscardIndex === index
                        ? 'ring-2 ring-green-500 scale-110'
                        : 'hover:scale-105'
                    }`}
                    onClick={() => setSelectedDiscardIndex(index)}
                  >
                    <Card card={card} />
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No cards in discard pile</p>
            )}
          </div>
        )}

        {/* Preview */}
        {preview && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold mb-2">Preview</h4>
            <p className="text-sm text-gray-600">
              {t('draw.cardsToDraw', { count: preview.total_cards })}
            </p>
          </div>
        )}

        {/* Actions */}
        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={handleClose}
            className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {t('draw.cancel')}
          </button>
          <button
            onClick={handleDraw}
            disabled={!selectedDrawType || (selectedDrawType === 'discard' && selectedDiscardIndex === null)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {t('draw.confirm')}
          </button>
        </div>
      </div>
    </div>
  );
};