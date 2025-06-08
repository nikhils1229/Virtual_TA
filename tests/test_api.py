import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_question_endpoint():
    """Test question answering endpoint"""
    question_data = {
        "question": "What is FastAPI?",
        "image": None
    }
    
    response = client.post("/api/", json=question_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "answer" in data
    assert "links" in data
    assert isinstance(data["links"], list)

def test_question_with_image():
    """Test question with base64 image"""
    # Simple base64 encoded 1x1 pixel image
    test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    question_data = {
        "question": "What do you see in this image?",
        "image": test_image
    }
    
    response = client.post("/api/", json=question_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "answer" in data
    assert "links" in data

def test_invalid_question():
    """Test handling of invalid requests"""
    response = client.post("/api/", json={})
    assert response.status_code == 422  # Validation error

def test_empty_question():
    """Test handling of empty question"""
    question_data = {
        "question": "",
        "image": None
    }
    
    response = client.post("/api/", json=question_data)
    assert response.status_code == 422  # Validation error
