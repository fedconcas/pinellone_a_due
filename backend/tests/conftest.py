import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_game_data():
    return {
        "player_names": ["Player 1", "Player 2"],
        "debug_mode": True
    }