import { create } from 'zustand';
import { GameState, Card, GameAction } from '../types/game.types';

interface GameStore {
  game: GameState | null;
  loading: boolean;
  error: string | null;
  debugMode: boolean;
  
  // Actions
  setGame: (game: GameState) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  toggleDebugMode: () => void;
  
  // API calls
  createGame: (playerNames: string[]) => Promise<string>;
  fetchGame: (gameId: string, playerId?: string) => Promise<any>;
  drawCards: (gameId: string, drawType: 'deck' | 'discard', cardIndex?: number) => Promise<void>;
  meldCards: (gameId: string, cardIndices: number[]) => Promise<void>;
  attachCard: (gameId: string, cardIndex: number, meldIndex: number) => Promise<void>;
  discardCard: (gameId: string, cardIndex: number) => Promise<void>;
  closeGame: (gameId: string) => Promise<void>;
}

const API_BASE = 'http://localhost:8000';

export const useGameStore = create<GameStore>((set, get) => ({
  game: null,
  loading: false,
  error: null,
  debugMode: false,
  
  setGame: (game) => set({ game }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  toggleDebugMode: () => set((state) => ({ debugMode: !state.debugMode })),
  
  createGame: async (playerNames: string[]) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/games`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_names: playerNames }),
      });
      
      if (!response.ok) throw new Error('Failed to create game');
      
      const data = await response.json();
      return data.game_id;
    } catch (error) {
      set({ error: (error as Error).message });
      throw error;
    } finally {
      set({ loading: false });
    }
  },
  
  fetchGame: async (gameId: string, playerId?: string) => {
    set({ loading: true, error: null });
    try {
      const url = new URL(`${API_BASE}/games/${gameId}`);
      if (playerId) {
        url.searchParams.append('player_id', playerId);
      }
      
      console.log('Fetching game with URL:', url.toString());
      console.log('Player ID:', playerId);
      
      const response = await fetch(url.toString());
      if (!response.ok) throw new Error('Game not found');
      
      const game = await response.json();
      console.log('Game response:', game);
      set({ game });
      return game;
    } catch (error) {
      set({ error: (error as Error).message });
      throw error;
    } finally {
      set({ loading: false });
    }
  },
  
  drawCards: async (gameId: string, drawType: 'deck' | 'discard', cardIndex?: number) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/draw`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          game_id: gameId,
          draw_type: drawType,
          card_index: cardIndex
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Invalid draw action');
      }
      
      const currentPlayerId = localStorage.getItem('player_id');
      await get().fetchGame(gameId, currentPlayerId || '0');
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ loading: false });
    }
  },
  
  meldCards: async (gameId: string, cardIndices: number[]) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/meld`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, card_indices: cardIndices }),
      });
      
      if (!response.ok) throw new Error('Invalid meld');
      
      const currentPlayerId = localStorage.getItem('player_id');
      await get().fetchGame(gameId, currentPlayerId || '0');
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ loading: false });
    }
  },
  
  attachCard: async (gameId: string, cardIndex: number, meldIndex: number) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/attach`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          game_id: gameId, 
          card_index: cardIndex, 
          meld_index: meldIndex 
        }),
      });
      
      if (!response.ok) throw new Error('Invalid attachment');
      
      const currentPlayerId = localStorage.getItem('player_id');
      await get().fetchGame(gameId, currentPlayerId || '0');
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ loading: false });
    }
  },
  
  discardCard: async (gameId: string, cardIndex: number) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/discard`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, card_index: cardIndex }),
      });
      
      if (!response.ok) throw new Error('Invalid discard');
      
      const currentPlayerId = localStorage.getItem('player_id');
      await get().fetchGame(gameId, currentPlayerId || '0');
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ loading: false });
    }
  },
  
  closeGame: async (gameId: string) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/games/${gameId}/close`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId }),
      });
      
      if (!response.ok) throw new Error('Cannot close game');
      
      const currentPlayerId = localStorage.getItem('player_id');
      await get().fetchGame(gameId, currentPlayerId || '0');
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ loading: false });
    }
  },
}));