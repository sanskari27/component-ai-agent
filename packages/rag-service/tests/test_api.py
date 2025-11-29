import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "status" in response.json()


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "embedding_model" in data


def test_search_endpoint(client):
    """Test search endpoint"""
    search_request = {
        "query": "button component",
        "limit": 5
    }
    
    response = client.post("/api/search", json=search_request)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data
    assert "query" in data
    assert isinstance(data["results"], list)


def test_suggest_endpoint(client):
    """Test suggest endpoint"""
    suggest_request = {
        "query": "user profile card",
        "limit": 3
    }
    
    response = client.post("/api/search/suggest", json=suggest_request)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_list_components_endpoint(client):
    """Test list components endpoint"""
    response = client.get("/api/components")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_component_endpoint(client):
    """Test create component endpoint"""
    component = {
        "id": "test-comp-1",
        "name": "TestButton",
        "description": "A test button component",
        "file_path": "/test/Button.tsx",
        "props": [
            {
                "name": "label",
                "type": "string",
                "required": True
            }
        ],
        "examples": [],
        "tags": ["button", "action"]
    }
    
    response = client.post("/api/components", json=component)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestButton"


def test_scan_endpoint_invalid_path(client):
    """Test scan endpoint with invalid path"""
    scan_request = {
        "folder_path": "/nonexistent/path",
        "include_storybooks": True,
        "recursive": True
    }
    
    response = client.post("/api/scan", json=scan_request)
    assert response.status_code == 400


def test_get_component_not_found(client):
    """Test getting a non-existent component"""
    response = client.get("/api/components/nonexistent-id")
    assert response.status_code == 404

