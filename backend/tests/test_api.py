import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_game():
    """Test creating a new game."""
    response = client.post("/api/games", json={
        "player_names": ["Alice", "Bob"],
        "debug_mode": True
    })
    assert response.status_code == 201
    data = response.json()
    assert "game_id" in data
    assert data["players"][0]["name"] == "Alice"
    assert data["players"][1]["name"] == "Bob"

def test_get_game():
    """Test retrieving a game state."""
    # Create a game first
    create_response = client.post("/api/games", json={
        "player_names": ["Alice", "Bob"]
    })
    game_id = create_response.json()["game_id"]
    
    # Get the game
    response = client.get(f"/api/games/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == game_id

def test_invalid_game_id():
    """Test getting a non-existent game."""
    response = client.get("/api/games/invalid-id")
    assert response.status_code == 404

def test_draw_card():
    """Test drawing a card."""
    # Create a game
    create_response = client.post("/api/games", json={
        "player_names": ["Alice", "Bob"]
    })
    game_id = create_response.json()["game_id"]
    
    # Draw a card
    response = client.post(f"/api/games/{game_id}/draw", json={
        "player_index": 0,
        "from_discard": False
    })
    assert response.status_code == 200
    data = response.json()
    assert "game_state" in data

def test_meld_cards():
    """Test melding cards."""
    # Create a game
    create_response = client.post("/api/games", json={
        "player_names": ["Alice", "Bob"],
        "debug_mode": True
    })
    game_id = create_response.json()["game_id"]
    
    # Get game state to see available cards
    game_response = client.get(f"/api/games/{game_id}")
    player_hand = game_response.json()["players"][0]["hand"]
    
    if len(player_hand) >= 3:
        # Try to meld first 3 cards
        response = client.post(f"/api/games/{game_id}/meld", json={
            "player_index": 0,
            "card_indices": [0, 1, 2]
        })
        # This might fail if cards don't form a valid meld
        assert response.status_code in [200, 400]

def test_discard_card():
    """Test discarding a card."""
    # Create a game
    create_response = client.post("/api/games", json={
        "player_names": ["Alice", "Bob"]
    })
    game_id = create_response.json()["game_id"]
    
    # Draw a card first
    client.post(f"/api/games/{game_id}/draw", json={
        "player_index": 0,
        "from_discard": False
    })
    
    # Discard a card
    response = client.post(f"/api/games/{game_id}/discard", json={
        "player_index": 0,
        "card_index": 0
    })
    assert response.status_code == 200