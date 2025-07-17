# Pinellone Game - Technical Architecture

## Project Structure

```
pinellone-modern/
├── frontend/                 # React + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameBoard.tsx
│   │   │   ├── PlayerHand.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── DiscardPile.tsx
│   │   │   ├── DebugPanel.tsx
│   │   │   └── GameControls.tsx
│   │   ├── store/
│   │   │   └── gameStore.ts
│   │   ├── types/
│   │   │   └── game.types.ts
│   │   ├── hooks/
│   │   │   └── useGame.ts
│   │   └── utils/
│   │       └── gameLogic.ts
│   ├── package.json
│   └── tsconfig.json
├── backend/                  # FastAPI + Python
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── card.py
│   │   │   ├── game.py
│   │   │   └── player.py
│   │   ├── services/
│   │   │   ├── game_service.py
│   │   │   ├── rules_engine.py
│   │   │   ├── scoring_service.py
│   │   │   └── deck_service.py
│   │   ├── api/
│   │   │   └── game_api.py
│   │   └── utils/
│   │       └── logger.py
│   ├── requirements.txt
│   └── tests/
├── shared/                   # Shared TypeScript definitions
│   └── types/
│       └── game.types.ts
└── docs/
    ├── RULES.md
    └── API.md
```

## Core Data Models

### Card System
- **Card**: rank, suit, is_joker, is_pinella
- **Deck**: 2 French decks (108 cards), no red 2s
- **Card Values**: A=15, 6-K=10, 3-5=5, Pinella=20, Joker=25

### Game State
- **Phase**: draw, play, discard
- **Players**: hand, melds, has_opened, score
- **Board**: deck, discard_pile, current_turn

### Rules Engine
- Scale validation (3+ consecutive same suit)
- Sestina requirement (6+ cards for closure)
- Joker/Pinella special handling
- Attachment rules
- Scoring system with bonuses

## API Endpoints

### Game Management
- POST /api/games - Create new game
- GET /api/games/{id} - Get game state
- POST /api/games/{id}/move - Make move
- GET /api/games/{id}/valid-moves - Get valid moves

### Debug
- POST /api/debug/force-move - Force specific move
- GET /api/debug/state - Get full debug state
- POST /api/debug/reset - Reset game

## Development Phases

### Phase 1: Core Models & Rules (2 days)
1. Implement card/deck models
2. Create rules engine
3. Basic game state management

### Phase 2: Backend API (2 days)
1. FastAPI setup
2. Game endpoints
3. Validation & error handling

### Phase 3: Frontend (3 days)
1. React setup with TypeScript
2. Game board components
3. Drag-and-drop interactions
4. Debug panel

### Phase 4: Polish & Testing (2 days)
1. AI implementation
2. Comprehensive tests
3. UI/UX improvements
4. Documentation