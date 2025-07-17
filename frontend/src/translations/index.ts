export interface Translation {
  [key: string]: string;
}

export interface Translations {
  [lang: string]: Translation;
}

export const translations: Translations = {
  en: {
    // Game UI
    'game.title': 'Pinellone Game',
    'game.create': 'Create New Game',
    'game.join': 'Join Game',
    'game.player1': 'Player 1 Name',
    'game.player2': 'Player 2 Name',
    'game.turn': '{player}\'s Turn',
    'game.gameOver': 'Game Over!',
    
    // Drawing
    'draw.title': 'Choose Drawing Method',
    'draw.deck': 'Draw 2 Cards from Deck',
    'draw.discard': 'Draw from Discard Pile',
    'draw.deckDescription': 'Draw 2 cards directly from the deck',
    'draw.discardDescription': 'Draw 1 card from deck + selected cards from discard',
    'draw.selectCard': 'Select a card from discard pile',
    'draw.cardsToDraw': 'Cards to draw: {count}',
    'draw.confirm': 'Confirm Selection',
    'draw.cancel': 'Cancel',
    
    // Game areas
    'game.deck': 'Deck',
    'game.discardPile': 'Discard Pile',
    'game.cardsRemaining': 'Cards remaining',
    'game.melds': 'Melds',
    'game.hand': 'Hand',
    
    // Actions
    'action.meld': 'Meld Cards',
    'action.attach': 'Attach to Meld',
    'action.discard': 'Discard Card',
    'action.close': 'Close Game',
    
    // Rules
    'rules.title': 'Game Rules',
    'rules.draw': 'Drawing Rules',
    'rules.drawDeck': 'Draw 2 cards from the deck',
    'rules.drawDiscard': 'Draw 1 card from deck + any cards from discard pile',
    'rules.meld': 'Create sets or runs of 3+ cards',
    'rules.close': 'Close the game with a sestina and 1 card left',
    
    // Errors
    'error.invalidDraw': 'Invalid draw action',
    'error.notYourTurn': 'Not your turn',
    'error.gameNotFound': 'Game not found',
    'error.invalidMeld': 'Invalid meld',
    'error.mustOpen': 'You must open before discarding',
    
    // Card names
    'card.joker': 'Joker',
    'card.two': 'Two',
    'suit.hearts': 'Hearts',
    'suit.diamonds': 'Diamonds',
    'suit.clubs': 'Clubs',
    'suit.spades': 'Spades',
  },
  it: {
    // Game UI
    'game.title': 'Gioco Pinellone',
    'game.create': 'Crea Nuova Partita',
    'game.join': 'Unisciti alla Partita',
    'game.player1': 'Nome Giocatore 1',
    'game.player2': 'Nome Giocatore 2',
    'game.turn': 'Turno di {player}',
    'game.gameOver': 'Partita Terminata!',
    
    // Drawing
    'draw.title': 'Scegli Metodo di Pesca',
    'draw.deck': 'Pesca 2 Carte dal Mazzo',
    'draw.discard': 'Pesca dal Mazzo Scarti',
    'draw.deckDescription': 'Pesca 2 carte direttamente dal mazzo',
    'draw.discardDescription': 'Pesca 1 dal mazzo + carte selezionate dagli scarti',
    'draw.selectCard': 'Seleziona una carta dal mazzo scarti',
    'draw.cardsToDraw': 'Carte da pescare: {count}',
    'draw.confirm': 'Conferma Selezione',
    'draw.cancel': 'Annulla',
    
    // Game areas
    'game.deck': 'Mazzo',
    'game.discardPile': 'Mazzo Scarti',
    'game.cardsRemaining': 'Carte rimanenti',
    'game.melds': 'Combinazioni',
    'game.hand': 'Mano',
    
    // Actions
    'action.meld': 'Crea Combinazione',
    'action.attach': 'Aggiungi a Combinazione',
    'action.discard': 'Scarta Carta',
    'action.close': 'Chiudi Partita',
    
    // Rules
    'rules.title': 'Regole del Gioco',
    'rules.draw': 'Regole di Pesca',
    'rules.drawDeck': 'Pesca 2 carte dal mazzo',
    'rules.drawDiscard': 'Pesca 1 dal mazzo + carte dal mazzo scarti',
    'rules.meld': 'Crea combinazioni di 3+ carte',
    'rules.close': 'Chiudi la partita con una sestina e 1 carta rimasta',
    
    // Errors
    'error.invalidDraw': 'Azione di pesca non valida',
    'error.notYourTurn': 'Non è il tuo turno',
    'error.gameNotFound': 'Partita non trovata',
    'error.invalidMeld': 'Combinazione non valida',
    'error.mustOpen': 'Devi aprire prima di scartare',
    
    // Card names
    'card.joker': 'Jolly',
    'card.two': 'Due',
    'suit.hearts': 'Cuori',
    'suit.diamonds': 'Quadri',
    'suit.clubs': 'Fiori',
    'suit.spades': 'Picche',
  }
};

export const translate = (key: string, lang: string, params?: Record<string, string | number>): string => {
  const translation = translations[lang]?.[key] || translations.en[key] || key;
  
  if (params) {
    return Object.entries(params).reduce((text, [param, value]) => {
      return text.replace(`{${param}}`, String(value));
    }, translation);
  }
  
  return translation;
};

export type Language = 'en' | 'it';