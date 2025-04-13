import pytest
import httpx
from src.main import app

@pytest.mark.asyncio
async def test_docs_page():
    """测试文档页面"""
    async with httpx.AsyncClient(base_url="http://test") as client:
        response = await client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "API 文档" in response.text

@pytest.mark.asyncio
async def test_redoc_page():
    """测试 ReDoc 页面"""
    async with httpx.AsyncClient(base_url="http://test") as client:
        response = await client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

@pytest.mark.asyncio
async def test_openapi_json():
    """测试 OpenAPI JSON"""
    async with httpx.AsyncClient(base_url="http://test") as client:
        response = await client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        assert "/api/v1/auth/client-credentials" in data["paths"]
        assert "/api/v1/auth/login" in data["paths"]
        assert "/api/v1/models/" in data["paths"]

@pytest.mark.asyncio
async def test_oauth2_redirect():
    """测试 OAuth2 重定向"""
    async with httpx.AsyncClient(base_url="http://test") as client:
        response = await client.get("/docs/oauth2-redirect")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"] 