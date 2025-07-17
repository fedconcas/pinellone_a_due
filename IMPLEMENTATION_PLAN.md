# Pinellone Implementation Plan - Detailed Steps

## Phase 1: Foundation (Days 1-2)

### Day 1: Core Models & Setup
- [ ] Create project structure
- [ ] Set up backend FastAPI project
- [ ] Set up frontend React project
- [ ] Create shared TypeScript definitions
- [ ] Implement Python data models (Card, Player, GameState)
- [ ] Create deck management system (2 decks, 108 cards)

### Day 2: Rules Engine
- [ ] Implement card validation utilities
- [ ] Create scale validation system
- [ ] Implement joker/pinella special rules
- [ ] Create scoring engine with bonuses
- [ ] Implement game closure validation

## Phase 2: Backend API (Days 3-4)

### Day 3: FastAPI Backend
- [ ] Set up FastAPI application
- [ ] Create game state management
- [ ] Implement REST API endpoints
- [ ] Add request validation
- [ ] Create error handling

### Day 4: Game Logic
- [ ] Implement turn-based flow
- [ ] Create move validation
- [ ] Add game state persistence
- [ ] Implement AI player interface
- [ ] Add comprehensive logging

## Phase 3: Frontend (Days 5-7)

### Day 5: React Setup
- [ ] Set up React + TypeScript
- [ ] Configure Tailwind CSS
- [ ] Create basic components
- [ ] Set up state management (Zustand)

### Day 6: Game Interface
- [ ] Implement card components
- [ ] Create game board layout
- [ ] Add drag-and-drop functionality
- [ ] Implement player hand display

### Day 7: UI Polish
- [ ] Create debug panel
- [ ] Add animations
- [ ] Implement game controls
- [ ] Add responsive design

## Phase 4: Testing & Polish (Days 8-9)

### Day 8: Testing
- [ ] Create comprehensive test suite
- [ ] Test all game rules
- [ ] Test edge cases
- [ ] Performance testing

### Day 9: Final Polish
- [ ] AI implementation
- [ ] Save/load functionality
- [ ] Documentation
- [ ] Deployment setup

## Technical Specifications

### Card System
- **Deck**: 108 cards (2 French decks)
- **Special Cards**: 4 Jokers, 2 Pinelle (black 2s)
- **Removed**: Red 2s (hearts & diamonds)
- **Distribution**: 15 cards per player

### Scoring
- **Card Values**:
  - 2-5: 5 points
  - 6-K: 10 points
  - Ace: 15 points
  - Pinella: 20 points
  - Joker: 25 points

### Bonuses
- **Closure**: +100 points
- **Clean Closure**: +200 points
- **Clean Sestina**: Double card values
- **Long Scales**: 7+ cards = x2, 10+ cards = x3
- **Pinnacolone**: +1500 points (A-K straight, 13 cards)

## Development Commands

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test