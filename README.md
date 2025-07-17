# Pinellone 2-Player Game

A modern web-based implementation of the Pinellone card game with all official rules.

## Features
- Complete Pinellone rules implementation
- Modern React frontend with drag-and-drop
- FastAPI backend with comprehensive game engine
- AI players for single-player mode
- Debug panel for development
- Save/load game state
- WebSocket support for future multiplayer

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Game Rules
See [RULES.md](RULES.md) for complete Pinellone rules.