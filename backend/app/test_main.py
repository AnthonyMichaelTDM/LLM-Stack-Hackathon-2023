"""Test the main.py file."""
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main() -> None:
    """Test the main endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CacheChat API"}
