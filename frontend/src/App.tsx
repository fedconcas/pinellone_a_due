import React, { useState, useEffect } from 'react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { sortableKeyboardCoordinates } from '@dnd-kit/sortable';
import { useGameStore } from './store/gameStore';
import { LanguageProvider } from './contexts/LanguageContext';
import { useLanguage } from './contexts/LanguageContext';
import { PlayerHand } from './components/PlayerHand';
import { GameControls } from './components/GameControls';
import { MeldsDisplay } from './components/MeldsDisplay';
import { DiscardPile } from './components/DiscardPile';
import { LanguageToggle } from './components/LanguageToggle';
import { DrawingSelectionModal } from './components/DrawingSelectionModal';
import './App.css';

function GameContent() {
  const { game, loading, error, createGame, fetchGame, drawCards, meldCards, discardCard } = useGameStore();
  const { t } = useLanguage();
  const [gameId, setGameId] = useState('');
  const [playerNames, setPlayerNames] = useState([t('game.player1'), t('game.player2')]);
  const [showDrawingModal, setShowDrawingModal] = useState(false);
  const [selectedCards, setSelectedCards] = useState<number[]>([]);
  const [selectedMeld, setSelectedMeld] = useState<number | null>(null);
  
  // Clear selected cards when turn changes
  useEffect(() => {
    setSelectedCards([]);
    setSelectedMeld(null);
  }, [game?.current_player_index]);
  
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleCreateGame = async () => {
    try {
      const newGameId = await createGame(playerNames);
      setGameId(newGameId);
      // First, fetch the game to get the actual player IDs
      const gameData = await fetchGame(newGameId);
      // Store player ID as the first player when creating
      if (gameData?.players[0]?.id) {
        localStorage.setItem('player_id', gameData.players[0].id);
        console.log('Created game with ID:', newGameId, 'Player ID:', gameData.players[0].id);
        // Fetch again with the correct player ID
        await fetchGame(newGameId, gameData.players[0].id);
      }
    } catch (err) {
      console.error('Failed to create game:', err);
    }
  };

  const handleJoinGame = async () => {
    if (gameId) {
      // First, fetch the game to get the actual player IDs
      const gameData = await fetchGame(gameId);
      // Store player ID as the second player when joining
      if (gameData?.players[1]?.id) {
        localStorage.setItem('player_id', gameData.players[1].id);
        console.log('Joining game with ID:', gameId, 'Player ID:', gameData.players[1].id);
        // Fetch again with the correct player ID
        await fetchGame(gameId, gameData.players[1].id);
      }
    }
  };

  const handleDraw = async (drawType: 'deck' | 'discard', discardIndex?: number) => {
    if (!game) return;
    
    try {
      await drawCards(game.id, drawType, discardIndex);
      setShowDrawingModal(false);
    } catch (err) {
      console.error('Failed to draw cards:', err);
    }
  };

  const handleDragEnd = async (event: any) => {
    const { active, over } = event;
    
    if (!over || !game) return;
    
    const activeId = active.id;
    const overId = over.id;
    
    // Parse card information from drag ID
    const cardMatch = activeId.match(/card-(\d+)-(\d+)/);
    if (!cardMatch) return;
    
    const playerIndex = parseInt(cardMatch[1]);
    const cardIndex = parseInt(cardMatch[2]);
    
    // Only allow current player to discard
    if (playerIndex !== game.current_player_index) {
      console.log('Only current player can discard');
      return;
    }
    
    // Handle discard pile drop
    if (overId === 'discard-pile') {
      try {
        await discardCard(game.id, cardIndex);
        // The discard action itself should handle the turn ending
        console.log('Card discarded successfully - turn should end');
        // Clear selected cards after successful discard
        setSelectedCards([]);
      } catch (err) {
        console.error('Failed to discard card:', err);
      }
    }
    
    // Handle meld area drop (can be extended)
    if (overId.startsWith('meld-')) {
      // This would be for attaching to melds
      // Implementation depends on specific meld structure
    }
  };

  if (!game) {
    return (
      <div className="min-h-screen bg-green-800 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
          <h1 className="text-3xl font-bold text-center mb-6 text-green-800">
            {t('game.title')}
          </h1>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">{t('game.player1')}</label>
              <input
                type="text"
                value={playerNames[0]}
                onChange={(e) => setPlayerNames([e.target.value, playerNames[1]])}
                className="w-full px-3 py-2 border rounded-md"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">{t('game.player2')}</label>
              <input
                type="text"
                value={playerNames[1]}
                onChange={(e) => setPlayerNames([playerNames[0], e.target.value])}
                className="w-full px-3 py-2 border rounded-md"
              />
            </div>
            
            <button
              onClick={handleCreateGame}
              disabled={loading}
              className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Creating...' : t('game.create')}
            </button>
            
            <div className="border-t pt-4">
              <label className="block text-sm font-medium mb-2">{t('game.join')}</label>
              <input
                type="text"
                placeholder="Enter game ID"
                value={gameId}
                onChange={(e) => setGameId(e.target.value)}
                className="w-full px-3 py-2 border rounded-md mb-2"
              />
              <button
                onClick={handleJoinGame}
                disabled={loading || !gameId}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {t('game.join')}
              </button>
            </div>
            
            {error && (
              <div className="text-red-600 text-sm text-center">{error}</div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <div className="min-h-screen bg-green-800">
        <div className="container mx-auto p-4">
          <h1 className="text-4xl font-bold text-white text-center mb-6">
            {t('game.title')} - {t('game.turn', { player: game.players[game.current_player_index]?.name })}
          </h1>
          
          {game.is_game_over && (
            <div className="bg-yellow-100 border-l-4 border-yellow-500 p-4 mb-6">
              <h2 className="text-xl font-bold">{t('game.gameOver')}</h2>
              <p>Final scores will be displayed here</p>
            </div>
          )}
          
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Main Game Area */}
            <div className="lg:col-span-3 space-y-6">
              {/* Player Hands */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {game.players.map((_, index) => (
                  <PlayerHand 
                    key={index} 
                    playerIndex={index}
                    selectedCards={index === game.current_player_index ? selectedCards : []}
                    onCardSelect={index === game.current_player_index ? (cardIndex) => {
                      setSelectedCards(prev => 
                        prev.includes(cardIndex)
                          ? prev.filter(i => i !== cardIndex)
                          : [...prev, cardIndex]
                      );
                    } : undefined}
                  />
                ))}
              </div>
              
              {/* Melds Display */}
              <MeldsDisplay />
              
              {/* Discard Pile and Deck */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <DiscardPile />
                <div className="bg-white rounded-lg p-4 shadow-lg">
                  <h3 className="text-lg font-bold mb-4">{t('game.deck')}</h3>
                  <div className="flex flex-col items-center">
                    <button
                      onClick={() => setShowDrawingModal(true)}
                      disabled={game.phase !== 'draw'}
                      className="w-16 h-24 bg-blue-600 border-2 border-blue-800 rounded-lg flex items-center justify-center text-white font-bold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {game.deck_count}
                    </button>
                    <p className="text-sm text-gray-600 mt-2">{t('game.cardsRemaining')}</p>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Sidebar */}
            <div className="space-y-4">
              <GameControls 
                selectedCards={selectedCards}
                setSelectedCards={setSelectedCards}
                selectedMeld={selectedMeld}
                setSelectedMeld={setSelectedMeld}
              />
              <DebugPanel />
            </div>
          </div>

          <DrawingSelectionModal
            isOpen={showDrawingModal}
            onClose={() => setShowDrawingModal(false)}
            onDraw={handleDraw}
          />
        </div>
      </div>
    </DndContext>
  );
}

// Updated DebugPanel component
function DebugPanel() {
  const { game, debugMode, toggleDebugMode } = useGameStore();
  
  return (
    <div className="bg-gray-100 rounded-lg p-4">
      <h3 className="font-bold mb-2">Debug Panel</h3>
      <button
        onClick={toggleDebugMode}
        className="w-full bg-gray-600 text-white py-2 px-4 rounded mb-4"
      >
        {debugMode ? 'Hide' : 'Show'} Debug Info
      </button>
      
      {debugMode && game && (
        <div className="text-xs">
          <pre className="max-h-64 overflow-auto">{JSON.stringify(game, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <LanguageProvider>
      <LanguageToggle />
      <GameContent />
    </LanguageProvider>
  );
}

export default App;