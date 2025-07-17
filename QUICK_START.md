# 🎮 Pinellone Game - Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Quick Setup

### 1. Clone and Navigate
```bash
cd pinellone-modern
```

### 2. Run Setup Script
```bash
python3 setup.py
```

### 3. Manual Setup (if script fails)

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

### 4. Start Development Servers

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

### 5. Play the Game
- Open http://localhost:3000 in your browser
- Create a new game or join an existing one
- Follow the on-screen instructions

## Development Commands

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### API Documentation
- Backend API docs: http://localhost:8000/docs
- Backend API schema: http://localhost:8000/openapi.json

## Project Structure
```
pinellone-modern/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── shared/           # Shared types and models
├── tests/            # Test files
├── docs/             # Documentation
└── setup.py          # Setup script
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Backend: Change port with `--port 8001`
   - Frontend: Vite will auto-select next available port

2. **Python dependencies**
   - Ensure Python 3.8+ is installed
   - Try: `pip install --upgrade pip`

3. **Node.js dependencies**
   - Clear cache: `npm cache clean --force`
   - Delete node_modules and reinstall

4. **CORS issues**
   - Check backend/.env has correct CORS_ORIGINS
   - Ensure frontend/.env has correct VITE_API_URL

## Game Rules Summary
- 2-player card game with 2 French decks (108 cards)
- Goal: Form sequences (scales) and close the game
- Must have a 6-card straight (sestina) to close
- Special cards: Jokers (25 pts) and Pinelle (20 pts)
- Detailed rules in README.md