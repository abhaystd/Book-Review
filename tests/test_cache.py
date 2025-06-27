from fastapi.testclient import TestClient
from server import app
from app.cache import mock_cache

client = TestClient(app)

def test_books_cache_miss_then_hit():
    mock_cache.clear()
    response = client.get("/books")  # First fetch → miss
    assert response.status_code == 200
    assert "books" in mock_cache

    response2 = client.get("/books")  # Second fetch → hit
    assert response2.status_code == 200