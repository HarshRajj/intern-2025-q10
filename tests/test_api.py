import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Q10 FastAPI Microservice"
    assert "timestamp" in data

def test_get_history():
    """Test the history endpoint."""
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_chat_endpoint_structure():
    """Test that chat endpoint accepts proper request structure."""
    response = client.post("/chat", json={"prompt": "Hello"})
    # Should not return 422 (validation error)
    assert response.status_code != 422
    # Should return 200 or handle gracefully
    if response.status_code == 200:
        data = response.json()
        assert "response" in data
        assert "tokens_used" in data

def test_chat_endpoint_without_api_key():
    """Test that chat endpoint works even without API key (for testing)."""
    response = client.post("/chat", json={"prompt": "Test message"})
    # Should work even without API key
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    # Should contain either actual response or test message
    assert len(data["response"]) > 0

def test_chat_endpoint_missing_prompt():
    """Test that chat endpoint validates required fields."""
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error

def test_export_csv():
    """Test CSV export endpoint."""
    response = client.get("/export_history_csv")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"

def test_export_txt():
    """Test text export endpoint."""
    response = client.get("/export_history_txt")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
