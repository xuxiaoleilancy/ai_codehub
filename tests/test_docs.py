import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    """Create a test client for each test"""
    client = TestClient(app)
    client.headers.update({"user-agent": "testclient"})
    return client

def test_docs_page(client):
    """Test the Swagger UI documentation page"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "API 文档" in response.text

def test_docs_page_not_found(client):
    """Test accessing a non-existent docs page"""
    response = client.get("/docs/nonexistent")
    assert response.status_code == 404

def test_redoc_page(client):
    """Test the ReDoc documentation page"""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_openapi_json(client):
    """Test the OpenAPI JSON endpoint"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    
    # Verify OpenAPI structure
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
    
    # Verify essential endpoints are documented
    assert "/auth/client-credentials" in data["paths"]
    assert "/auth/login" in data["paths"]
    assert "/models/" in data["paths"]
    
    # Verify OpenAPI version
    assert data["openapi"].startswith("3.")

def test_openapi_yaml(client):
    """Test the OpenAPI YAML endpoint"""
    response = client.get("/openapi.yaml")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/yaml"

def test_oauth2_redirect(client):
    """Test the OAuth2 redirect endpoint"""
    response = client.get("/docs/oauth2-redirect")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_docs_with_invalid_accept_header(client):
    """Test docs endpoint with invalid Accept header"""
    response = client.get("/docs", headers={"Accept": "invalid/type"})
    assert response.status_code == 200  # Should still return HTML
    assert response.headers["content-type"] == "text/html; charset=utf-8" 