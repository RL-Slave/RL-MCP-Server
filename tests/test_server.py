"""Tests für MCP Server."""

import pytest
from fastapi.testclient import TestClient

from mcp_server.server import app


@pytest.fixture
def client():
    """Test-Client für FastAPI."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test Root-Endpunkt."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ollama MCP Server"
    assert "tools_count" in data


def test_health_endpoint(client):
    """Test Health-Endpunkt."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_list_tools(client):
    """Test Tools-Liste."""
    response = client.post("/mcp/tools/list")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) > 0


def test_tools_have_required_fields(client):
    """Test dass alle Tools die erforderlichen Felder haben."""
    response = client.post("/mcp/tools/list")
    tools = response.json()["tools"]
    
    for tool in tools:
        assert "name" in tool
        assert "description" in tool
        assert "inputSchema" in tool
        assert tool["name"].startswith("ollama_")

