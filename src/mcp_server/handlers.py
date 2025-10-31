"""Request-Handler für MCP Server."""

import asyncio
import json
from typing import Any, AsyncGenerator, Dict, List, Optional

from mcp_server.client import OllamaClient
from mcp_server.exceptions import MCPError, OllamaAPIError, ValidationError
from mcp_server.utils.formatting import (
    format_chat_response,
    format_embedding_response,
    format_error,
    format_generate_response,
    format_model_list,
)
from mcp_server.utils.session import SessionManager
from mcp_server.utils.validation import validate_model_name


class ToolHandler:
    """Handler für Tool-Aufrufe."""

    def __init__(self, ollama_client: OllamaClient, session_manager: SessionManager):
        """Initialisiert den Tool Handler."""
        self.client = ollama_client
        self.sessions = session_manager

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Führt ein Tool aus."""
        try:
            if tool_name == "ollama_check_health":
                return await self._check_health()
            elif tool_name == "ollama_list_models":
                return await self._list_models()
            elif tool_name == "ollama_show_model":
                return await self._show_model(arguments)
            elif tool_name == "ollama_pull_model":
                return await self._pull_model(arguments)
            elif tool_name == "ollama_delete_model":
                return await self._delete_model(arguments)
            elif tool_name == "ollama_copy_model":
                return await self._copy_model(arguments)
            elif tool_name == "ollama_create_model":
                return await self._create_model(arguments)
            elif tool_name == "ollama_generate":
                return await self._generate(arguments)
            elif tool_name == "ollama_generate_stream":
                return await self._generate_stream(arguments)
            elif tool_name == "ollama_chat":
                return await self._chat(arguments)
            elif tool_name == "ollama_chat_stream":
                return await self._chat_stream(arguments)
            elif tool_name == "ollama_embeddings":
                return await self._embeddings(arguments)
            elif tool_name == "ollama_create_embeddings":
                return await self._create_embeddings(arguments)
            elif tool_name == "ollama_list_processes":
                return await self._list_processes()
            elif tool_name == "ollama_check_blobs":
                return await self._check_blobs(arguments)
            elif tool_name == "ollama_get_version":
                return await self._get_version()
            elif tool_name == "ollama_update_model":
                return await self._update_model(arguments)
            elif tool_name == "ollama_get_modelfile":
                return await self._get_modelfile(arguments)
            elif tool_name == "ollama_get_models_info":
                return await self._get_models_info()
            elif tool_name == "ollama_validate_model":
                return await self._validate_model(arguments)
            elif tool_name == "ollama_get_model_size":
                return await self._get_model_size(arguments)
            elif tool_name == "ollama_search_models":
                return await self._search_models(arguments)
            elif tool_name == "ollama_save_context":
                return await self._save_context(arguments)
            elif tool_name == "ollama_load_context":
                return await self._load_context(arguments)
            elif tool_name == "ollama_clear_context":
                return await self._clear_context(arguments)
            elif tool_name == "ollama_batch_generate":
                return await self._batch_generate(arguments)
            elif tool_name == "ollama_compare_models":
                return await self._compare_models(arguments)
            else:
                raise MCPError(f"Unbekanntes Tool: {tool_name}")
        except Exception as e:
            return format_error(e)

    async def _check_health(self) -> Dict[str, Any]:
        """Health-Check."""
        try:
            await self.client.list_models()
            return {"status": "healthy", "ollama_connected": True}
        except Exception:
            return {"status": "unhealthy", "ollama_connected": False}

    async def _list_models(self) -> Dict[str, Any]:
        """Listet Modelle auf."""
        response = await self.client.list_models()
        return format_model_list(response)

    async def _show_model(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Zeigt Modell-Details."""
        model = validate_model_name(args.get("model", ""))
        return await self.client.show_model(model)

    async def _pull_model(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Lädt ein Modell herunter."""
        model = validate_model_name(args.get("model", ""))
        insecure = args.get("insecure", False)

        result = {"status": "downloading", "model": model}
        chunks = []
        async for chunk in self.client.pull_model(model, insecure):
            chunks.append(chunk)
            if chunk.get("status") == "success":
                result["status"] = "success"
                break
            elif chunk.get("error"):
                result["status"] = "error"
                result["error"] = chunk.get("error")
                break

        return result

    async def _delete_model(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Löscht ein Modell."""
        model = validate_model_name(args.get("model", ""))
        return await self.client.delete_model(model)

    async def _copy_model(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Kopiert ein Modell."""
        source = validate_model_name(args.get("source", ""))
        destination = validate_model_name(args.get("destination", ""))
        return await self.client.copy_model(source, destination)

    async def _create_model(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Erstellt ein Modell."""
        model = validate_model_name(args.get("model", ""))
        modelfile = args.get("modelfile", "")
        if not modelfile:
            raise ValidationError("modelfile ist erforderlich")

        result = {"status": "creating", "model": model}
        async for chunk in self.client.create_model(model, modelfile):
            if chunk.get("status") == "success":
                result["status"] = "success"
                break
            elif chunk.get("error"):
                result["status"] = "error"
                result["error"] = chunk.get("error")
                break

        return result

    async def _generate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generiert Text."""
        model = validate_model_name(args.get("model", ""))
        prompt = args.get("prompt", "")
        if not prompt:
            raise ValidationError("prompt ist erforderlich")

        system = args.get("system")
        template = args.get("template")
        context = args.get("context")
        options = args.get("options", {})

        async for response in self.client.generate(
            model, prompt, system, template, context, stream=False, options=options
        ):
            return format_generate_response(response)

    async def _generate_stream(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generiert Text im Streaming-Modus."""
        model = validate_model_name(args.get("model", ""))
        prompt = args.get("prompt", "")
        if not prompt:
            raise ValidationError("prompt ist erforderlich")

        system = args.get("system")
        template = args.get("template")
        context = args.get("context")
        options = args.get("options", {})

        chunks = []
        async for chunk in self.client.generate(
            model, prompt, system, template, context, stream=True, options=options
        ):
            chunks.append(format_generate_response(chunk))
        return chunks

    async def _chat(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Chat-Kompletierung."""
        model = validate_model_name(args.get("model", ""))
        messages = args.get("messages", [])
        if not messages:
            raise ValidationError("messages sind erforderlich")

        options = args.get("options", {})

        async for response in self.client.chat(model, messages, stream=False, options=options):
            return format_chat_response(response)

    async def _chat_stream(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chat im Streaming-Modus."""
        model = validate_model_name(args.get("model", ""))
        messages = args.get("messages", [])
        if not messages:
            raise ValidationError("messages sind erforderlich")

        options = args.get("options", {})

        chunks = []
        async for chunk in self.client.chat(model, messages, stream=True, options=options):
            chunks.append(format_chat_response(chunk))
        return chunks

    async def _embeddings(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generiert Embeddings."""
        model = validate_model_name(args.get("model", ""))
        prompt = args.get("prompt", "")
        if not prompt:
            raise ValidationError("prompt ist erforderlich")

        options = args.get("options", {})
        response = await self.client.embeddings(model, prompt, options)
        return format_embedding_response(response)

    async def _create_embeddings(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Erstellt Embeddings für mehrere Texte."""
        model = validate_model_name(args.get("model", ""))
        prompts = args.get("prompts", [])
        if not prompts:
            raise ValidationError("prompts sind erforderlich")

        options = args.get("options", {})
        results = []
        for prompt in prompts:
            response = await self.client.embeddings(model, prompt, options)
            results.append(format_embedding_response(response))
        return results

    async def _list_processes(self) -> Dict[str, Any]:
        """Listet Prozesse auf."""
        return await self.client.list_processes()

    async def _check_blobs(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Prüft Blob."""
        digest = args.get("digest", "")
        if not digest:
            raise ValidationError("digest ist erforderlich")
        exists = await self.client.check_blob(digest)
        return {"digest": digest, "exists": exists}

    async def _get_version(self) -> Dict[str, Any]:
        """Ruft Version ab."""
        return await self.client.get_version()

    async def _update_model(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Aktualisiert ein Modell."""
        model = validate_model_name(args.get("model", ""))
        modelfile = args.get("modelfile", "")
        if not modelfile:
            raise ValidationError("modelfile ist erforderlich")

        # update_model ist im Grunde create_model mit overwrite
        result = {"status": "updating", "model": model}
        async for chunk in self.client.create_model(model, modelfile):
            if chunk.get("status") == "success":
                result["status"] = "success"
                break
            elif chunk.get("error"):
                result["status"] = "error"
                result["error"] = chunk.get("error")
                break

        return result

    async def _get_modelfile(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Ruft Modelfile ab."""
        model = validate_model_name(args.get("model", ""))
        response = await self.client.show_model(model)
        modelfile = response.get("modelfile", "")
        return {"model": model, "modelfile": modelfile}

    async def _get_models_info(self) -> Dict[str, Any]:
        """Ruft Informationen über alle Modelle ab."""
        models_response = await self.client.list_models()
        models = models_response.get("models", [])

        models_info = []
        for model_data in models:
            model_name = model_data.get("name", "")
            try:
                model_details = await self.client.show_model(model_name)
                models_info.append(
                    {
                        "name": model_name,
                        "size": model_data.get("size", 0),
                        "modified_at": model_data.get("modified_at", ""),
                        "details": model_details,
                    }
                )
            except Exception:
                models_info.append(
                    {
                        "name": model_name,
                        "size": model_data.get("size", 0),
                        "modified_at": model_data.get("modified_at", ""),
                        "details": None,
                    }
                )

        return {"models": models_info, "count": len(models_info)}

    async def _validate_model(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Validiert ein Modell."""
        model = validate_model_name(args.get("model", ""))
        try:
            model_info = await self.client.show_model(model)
            return {
                "valid": True,
                "model": model,
                "details": model_info,
            }
        except Exception as e:
            return {
                "valid": False,
                "model": model,
                "error": str(e),
            }

    async def _get_model_size(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Ruft Modell-Größe ab."""
        model = validate_model_name(args.get("model", ""))
        models_response = await self.client.list_models()
        models = models_response.get("models", [])

        for model_data in models:
            if model_data.get("name") == model:
                size_bytes = model_data.get("size", 0)
                size_mb = size_bytes / (1024 * 1024)
                size_gb = size_bytes / (1024 * 1024 * 1024)
                return {
                    "model": model,
                    "size_bytes": size_bytes,
                    "size_mb": round(size_mb, 2),
                    "size_gb": round(size_gb, 2),
                    "size_human": f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.2f} MB",
                }

        raise ValidationError(f"Modell {model} nicht gefunden")

    async def _search_models(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Durchsucht Modelle."""
        query = args.get("query", "").lower()
        if not query:
            raise ValidationError("query ist erforderlich")

        models_response = await self.client.list_models()
        models = models_response.get("models", [])

        matching_models = [
            model_data
            for model_data in models
            if query in model_data.get("name", "").lower()
        ]

        return {"query": query, "models": matching_models, "count": len(matching_models)}

    async def _save_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Speichert Kontext."""
        session_id = args.get("session_id", "")
        if not session_id:
            raise ValidationError("session_id ist erforderlich")

        messages = args.get("messages", [])
        if not messages:
            raise ValidationError("messages sind erforderlich")

        success = self.sessions.save_context(session_id, messages)
        return {"session_id": session_id, "saved": success}

    async def _load_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Lädt Kontext."""
        session_id = args.get("session_id", "")
        if not session_id:
            raise ValidationError("session_id ist erforderlich")

        messages = self.sessions.load_context(session_id)
        return {"session_id": session_id, "messages": messages or []}

    async def _clear_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Löscht Kontext."""
        session_id = args.get("session_id", "")
        if not session_id:
            raise ValidationError("session_id ist erforderlich")

        success = self.sessions.clear_context(session_id)
        return {"session_id": session_id, "cleared": success}

    async def _batch_generate(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Batch-Generierung."""
        model = validate_model_name(args.get("model", ""))
        prompts = args.get("prompts", [])
        if not prompts:
            raise ValidationError("prompts sind erforderlich")

        options = args.get("options", {})

        results = []
        for prompt in prompts:
            async for response in self.client.generate(
                model, prompt, stream=False, options=options
            ):
                results.append(format_generate_response(response))
                break

        return results

    async def _compare_models(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Vergleicht Modelle."""
        models = args.get("models", [])
        if not models or len(models) < 2:
            raise ValidationError("mindestens 2 Modelle erforderlich")

        prompt = args.get("prompt", "")
        if not prompt:
            raise ValidationError("prompt ist erforderlich")

        options = args.get("options", {})

        results = {}
        for model_name in models:
            try:
                validate_model_name(model_name)
                async for response in self.client.generate(
                    model_name, prompt, stream=False, options=options
                ):
                    results[model_name] = format_generate_response(response)
                    break
            except Exception as e:
                results[model_name] = {"error": str(e)}

        return {"prompt": prompt, "results": results}

