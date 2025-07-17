export interface Card {
  rank: string;
  suit: string;
  card_type: 'normal' | 'joker' | 'pinella';
  is_wild: boolean;
  value: number;
}

export interface Player {
  id: string;
  name: string;
  hand_count: number;
  hand?: Card[]; // Actual cards for the owning player
  melds: Card[][];
  has_opened: boolean;
  score: number;
  can_close: boolean;
}

export interface GameState {
  id: string;
  players: Player[];
  current_player_index: number;
  phase: 'draw' | 'play' | 'discard';
  deck_count: number;
  discard_pile: Card[];
  is_game_over: boolean;
}

export interface CreateGameRequest {
  player_names: string[];
}

export interface GameAction {
  game_id: string;
  type: 'draw' | 'meld' | 'attach' | 'discard' | 'close';
  data?: any;
}