"""Tests für Ollama Client."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from mcp_server.client import OllamaClient
from mcp_server.exceptions import OllamaConnectionError, OllamaAPIError


@pytest.fixture
def client():
    """Test-Client."""
    with patch("mcp_server.client.get_config") as mock_config:
        mock_config.return_value = type(
            "Config",
            (),
            {
                "ollama_base_url": "http://localhost:11434",
                "ollama_timeout": 60,
            },
        )()
        return OllamaClient()


@pytest.mark.asyncio
async def test_list_models(client):
    """Test Modell-Liste."""
    with patch("httpx.AsyncClient.request") as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {"models": []}
        mock_request.return_value = mock_response
        
        result = await client.list_models()
        assert "models" in result


@pytest.mark.asyncio
async def test_connection_error(client):
    """Test Verbindungsfehler."""
    with patch("httpx.AsyncClient.request") as mock_request:
        mock_request.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception):
            await client.list_models()

