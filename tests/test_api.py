import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Market Data Service is running" in response.json()["message"]

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "timestamp" in response.json()

def test_get_latest_price_valid_symbol():
    """Test getting price for valid symbol"""
    response = client.get("/prices/latest?symbol=AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "price" in data
    assert "timestamp" in data
    assert "provider" in data

def test_get_latest_price_invalid_symbol():
    """Test getting price for invalid symbol"""
    response = client.get("/prices/latest?symbol=INVALID")
    assert response.status_code == 404

def test_poll_endpoint():
    """Test the polling endpoint"""
    payload = {
        "symbols": ["AAPL", "MSFT"],
        "interval": 60,
        "provider": "yahoo_finance"
    }
    response = client.post("/prices/poll", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "accepted"
    assert data["config"]["symbols"] == ["AAPL", "MSFT"]