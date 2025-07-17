from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .services.game_service import GameService

app = FastAPI(title="Pinellone Game API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_service = GameService()

class CreateGameRequest(BaseModel):
    player_names: List[str]

class DrawRequest(BaseModel):
    game_id: str
    draw_type: str  # 'deck' or 'discard'
    card_index: Optional[int] = None  # Required for discard draws

class DrawPreviewRequest(BaseModel):
    game_id: str
    draw_type: str
    card_index: Optional[int] = None

class MeldRequest(BaseModel):
    game_id: str
    card_indices: List[int]

class AttachRequest(BaseModel):
    game_id: str
    card_index: int
    meld_index: int

class DiscardRequest(BaseModel):
    game_id: str
    card_index: int

@app.get("/")
async def root():
    return {"message": "Pinellone Game API"}

@app.post("/games")
async def create_game(request: CreateGameRequest):
    """Create a new game"""
    try:
        game = game_service.create_game(request.player_names)
        return {"game_id": game.id, "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/games/{game_id}")
async def get_game(game_id: str, player_id: Optional[str] = None):
    """Get game state
    
    Args:
        game_id: The game ID
        player_id: Optional player ID to expose hand details to owning player
    """
    game_state = game_service.get_game_state(game_id, player_id)
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not found")
    return game_state

@app.post("/games/{game_id}/draw")
async def draw_card(request: DrawRequest):
    """Draw cards according to Pinellone rules"""
    if request.draw_type not in ['deck', 'discard']:
        raise HTTPException(status_code=400, detail="draw_type must be 'deck' or 'discard'")
    
    if request.draw_type == 'discard' and request.card_index is None:
        raise HTTPException(status_code=400, detail="card_index required for discard pile draw")
    
    success = game_service.draw_cards(request.game_id, request.draw_type, request.card_index)
    
    if not success:
        raise HTTPException(status_code=400, detail="Invalid draw action")
    
    return {"status": "success"}

@app.post("/games/{game_id}/draw-preview")
async def get_draw_preview(request: DrawPreviewRequest):
    """Preview what cards would be drawn"""
    preview = game_service.get_draw_preview(request.game_id, request.draw_type, request.card_index)
    if not preview:
        raise HTTPException(status_code=400, detail="Invalid preview request")
    
    return preview

@app.post("/games/{game_id}/meld")
async def meld_cards(request: MeldRequest):
    """Meld cards"""
    success = game_service.meld_cards(request.game_id, request.card_indices)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid meld")
    
    return {"status": "success"}

@app.post("/games/{game_id}/attach")
async def attach_card(request: AttachRequest):
    """Attach card to existing meld"""
    success = game_service.attach_card(request.game_id, request.card_index, request.meld_index)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid attachment")
    
    return {"status": "success"}

@app.post("/games/{game_id}/discard")
async def discard_card(request: DiscardRequest):
    """Discard a card"""
    success = game_service.discard_card(request.game_id, request.card_index)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid discard")
    
    return {"status": "success"}

@app.post("/games/{game_id}/close")
async def close_game(game_id: str):
    """Close the game"""
    success = game_service.close_game(game_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot close game")
    
    return {"status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)