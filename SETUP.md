# Pinellone Game Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Backend Setup

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Quick Start

1. Start the backend server (runs on http://localhost:8000)
2. Start the frontend dev server (runs on http://localhost:3000)
3. Create a new game with two player names
4. Play Pinellone!

## Development

### Backend Development
- Game logic is in `backend/app/services/`
- Models are in `backend/app/models/`
- API endpoints are in `backend/app/main.py`

### Frontend Development
- React components in `frontend/src/components/`
- State management with Zustand in `frontend/src/store/`
- Types in `frontend/src/types/`

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Production Build

### Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
npm run preview