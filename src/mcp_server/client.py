"""Ollama API Client für MCP Server."""

import json
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx

from mcp_server.config import get_config
from mcp_server.exceptions import OllamaAPIError, OllamaConnectionError


class OllamaClient:
    """Client für Ollama API."""

    def __init__(self, config=None):
        """Initialisiert den Ollama Client."""
        self.config = config or get_config()
        self.base_url = self.config.ollama_base_url
        self.timeout = self.config.ollama_timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Gibt den HTTP Client zurück (lazy initialization)."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    async def close(self):
        """Schließt den HTTP Client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Führt eine HTTP-Anfrage an Ollama API durch."""
        try:
            client = await self._get_client()
            response = await client.request(
                method=method,
                url=endpoint,
                json=json_data,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise OllamaConnectionError(f"Verbindung zu Ollama fehlgeschlagen: {e}")
        except httpx.HTTPStatusError as e:
            raise OllamaAPIError(
                f"Ollama API Fehler: {e.response.text}",
                status_code=e.response.status_code,
            )
        except Exception as e:
            raise OllamaAPIError(f"Unerwarteter Fehler: {e}")

    async def list_models(self) -> Dict[str, Any]:
        """Listet alle verfügbaren Modelle auf."""
        return await self._request("GET", "/api/tags")

    async def show_model(self, model: str) -> Dict[str, Any]:
        """Zeigt Details zu einem Modell."""
        return await self._request("POST", "/api/show", json_data={"model": model})

    async def pull_model(
        self, model: str, insecure: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Lädt ein Modell herunter (Streaming)."""
        client = await self._get_client()
        async with client.stream(
            "POST",
            "/api/pull",
            json={"name": model, "insecure": insecure},
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue

    async def delete_model(self, model: str) -> Dict[str, Any]:
        """Löscht ein Modell."""
        return await self._request("DELETE", "/api/delete", json_data={"name": model})

    async def copy_model(self, source: str, destination: str) -> Dict[str, Any]:
        """Kopiert ein Modell."""
        return await self._request(
            "POST",
            "/api/copy",
            json_data={"source": source, "destination": destination},
        )

    async def create_model(
        self, model: str, modelfile: str, stream: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Erstellt ein Modell aus einer Modelfile."""
        if stream:
            client = await self._get_client()
            async with client.stream(
                "POST",
                "/api/create",
                json={"name": model, "modelfile": modelfile, "stream": stream},
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            continue
        else:
            result = await self._request(
                "POST",
                "/api/create",
                json_data={"name": model, "modelfile": modelfile},
            )
            yield result

    async def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        template: Optional[str] = None,
        context: Optional[List[int]] = None,
        stream: bool = False,
        options: Optional[Dict[str, Any]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generiert Text mit einem Modell."""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
        }

        if system:
            payload["system"] = system
        if template:
            payload["template"] = template
        if context:
            payload["context"] = context
        if options:
            payload["options"] = options

        if stream:
            client = await self._get_client()
            async with client.stream("POST", "/api/generate", json=payload) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            continue
        else:
            result = await self._request("POST", "/api/generate", json_data=payload)
            yield result

    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = False,
        options: Optional[Dict[str, Any]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Führt einen Chat mit einem Modell."""
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }

        if options:
            payload["options"] = options

        if stream:
            client = await self._get_client()
            async with client.stream("POST", "/api/chat", json=payload) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            continue
        else:
            result = await self._request("POST", "/api/chat", json_data=payload)
            yield result

    async def embeddings(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generiert Embeddings für einen Text."""
        payload = {"model": model, "prompt": prompt}
        if options:
            payload["options"] = options
        return await self._request("POST", "/api/embeddings", json_data=payload)

    async def list_processes(self) -> Dict[str, Any]:
        """Listet laufende Prozesse auf."""
        return await self._request("GET", "/api/ps")

    async def check_blob(self, digest: str) -> bool:
        """Prüft ob ein Blob vorhanden ist."""
        try:
            client = await self._get_client()
            response = await client.head(f"/api/blobs/{digest}")
            return response.status_code == 200
        except Exception:
            return False

    async def get_version(self) -> Dict[str, Any]:
        """Ruft die Ollama-Version ab."""
        return await self._request("GET", "/api/version")

