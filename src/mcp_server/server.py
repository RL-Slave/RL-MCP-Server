"""Haupt-MCP Server Implementierung."""

import asyncio
import json
import logging
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn import run

from mcp_server.client import OllamaClient
from mcp_server.config import Config, get_config
from mcp_server.handlers import ToolHandler
from mcp_server.utils.session import SessionManager

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Globale Instanzen
config: Config = None
ollama_client: OllamaClient = None
session_manager: SessionManager = None
tool_handler: ToolHandler = None


from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan-Context für Startup/Shutdown."""
    # Startup
    global config, ollama_client, session_manager, tool_handler

    config = get_config()
    ollama_client = OllamaClient(config)
    session_manager = SessionManager(config)
    tool_handler = ToolHandler(ollama_client, session_manager)

    logger.info(f"MCP Server startet auf {config.mcp_host}:{config.mcp_port}")
    logger.info(f"Ollama API: {config.ollama_base_url}")

    yield

    # Shutdown
    if ollama_client:
        await ollama_client.close()
    logger.info("MCP Server beendet")


app = FastAPI(title="Ollama MCP Server", version="0.1.0", lifespan=lifespan)

# CORS für Remote-Zugriff
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Tool-Definitionen für MCP
TOOLS = [
    {
        "name": "ollama_check_health",
        "description": "Prüft ob Ollama-Server erreichbar und funktionsfähig ist",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "ollama_list_models",
        "description": "Listet alle verfügbaren Ollama-Modelle mit Details auf",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "ollama_show_model",
        "description": "Zeigt detaillierte Informationen zu einem spezifischen Modell an",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
            },
            "required": ["model"],
        },
    },
    {
        "name": "ollama_pull_model",
        "description": "Lädt ein Modell aus dem Ollama-Registry herunter",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "insecure": {"type": "boolean", "description": "Unsichere Registry verwenden"},
            },
            "required": ["model"],
        },
    },
    {
        "name": "ollama_delete_model",
        "description": "Löscht ein Modell vom lokalen System",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
            },
            "required": ["model"],
        },
    },
    {
        "name": "ollama_copy_model",
        "description": "Kopiert ein Modell unter neuem Namen",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Quell-Modellname"},
                "destination": {"type": "string", "description": "Ziel-Modellname"},
            },
            "required": ["source", "destination"],
        },
    },
    {
        "name": "ollama_create_model",
        "description": "Erstellt ein neues Modell aus einer Modelfile",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "modelfile": {"type": "string", "description": "Modelfile-Inhalt"},
            },
            "required": ["model", "modelfile"],
        },
    },
    {
        "name": "ollama_generate",
        "description": "Generiert Text mit einem Ollama-Modell basierend auf einem Prompt",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "prompt": {"type": "string", "description": "Eingabe-Prompt"},
                "system": {"type": "string", "description": "System-Prompt"},
                "template": {"type": "string", "description": "Prompt-Template"},
                "context": {"type": "array", "description": "Kontext-Array"},
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["model", "prompt"],
        },
    },
    {
        "name": "ollama_generate_stream",
        "description": "Generiert Text im Streaming-Modus (Token für Token)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "prompt": {"type": "string", "description": "Eingabe-Prompt"},
                "system": {"type": "string", "description": "System-Prompt"},
                "template": {"type": "string", "description": "Prompt-Template"},
                "context": {"type": "array", "description": "Kontext-Array"},
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["model", "prompt"],
        },
    },
    {
        "name": "ollama_chat",
        "description": "Führt eine Chat-Konversation mit einem Modell",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "messages": {
                    "type": "array",
                    "description": "Array von Chat-Nachrichten",
                    "items": {
                        "type": "object",
                        "properties": {
                            "role": {"type": "string", "enum": ["system", "user", "assistant"]},
                            "content": {"type": "string"},
                        },
                    },
                },
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["model", "messages"],
        },
    },
    {
        "name": "ollama_chat_stream",
        "description": "Führt Chat im Streaming-Modus durch",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "messages": {
                    "type": "array",
                    "description": "Array von Chat-Nachrichten",
                    "items": {
                        "type": "object",
                        "properties": {
                            "role": {"type": "string", "enum": ["system", "user", "assistant"]},
                            "content": {"type": "string"},
                        },
                    },
                },
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["model", "messages"],
        },
    },
    {
        "name": "ollama_embeddings",
        "description": "Generiert Embedding-Vektoren für einen gegebenen Text",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "prompt": {"type": "string", "description": "Text für Embedding"},
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["model", "prompt"],
        },
    },
    {
        "name": "ollama_create_embeddings",
        "description": "Erstellt Embeddings für mehrere Texte gleichzeitig",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "prompts": {"type": "array", "items": {"type": "string"}, "description": "Array von Texten"},
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["model", "prompts"],
        },
    },
    {
        "name": "ollama_list_processes",
        "description": "Listet alle laufenden Modell-Inferenz-Prozesse auf",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "ollama_check_blobs",
        "description": "Prüft ob ein Blob (Modell-Teil) vorhanden ist",
        "inputSchema": {
            "type": "object",
            "properties": {
                "digest": {"type": "string", "description": "Blob-Digest"},
            },
            "required": ["digest"],
        },
    },
    {
        "name": "ollama_get_version",
        "description": "Ruft die Ollama-Server-Version ab",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "ollama_update_model",
        "description": "Aktualisiert ein bestehendes Modell mit neuer Modelfile",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "modelfile": {"type": "string", "description": "Neue Modelfile-Definition"},
            },
            "required": ["model", "modelfile"],
        },
    },
    {
        "name": "ollama_get_modelfile",
        "description": "Ruft die Modelfile-Konfiguration eines Modells ab",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
            },
            "required": ["model"],
        },
    },
    {
        "name": "ollama_get_models_info",
        "description": "Ruft detaillierte Informationen über alle Modelle ab",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "ollama_validate_model",
        "description": "Validiert ob ein Modell korrekt installiert und funktionsfähig ist",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
            },
            "required": ["model"],
        },
    },
    {
        "name": "ollama_get_model_size",
        "description": "Ruft die Speichergröße eines Modells ab",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
            },
            "required": ["model"],
        },
    },
    {
        "name": "ollama_search_models",
        "description": "Durchsucht verfügbare Modelle nach Namen oder Tags",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Suchbegriff"},
                "remote": {"type": "boolean", "description": "Auch Remote-Registry durchsuchen"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "ollama_save_context",
        "description": "Speichert Chat-Kontext für spätere Verwendung",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "Session-ID"},
                "messages": {
                    "type": "array",
                    "description": "Chat-Messages",
                    "items": {
                        "type": "object",
                        "properties": {
                            "role": {"type": "string"},
                            "content": {"type": "string"},
                        },
                    },
                },
            },
            "required": ["session_id", "messages"],
        },
    },
    {
        "name": "ollama_load_context",
        "description": "Lädt gespeicherten Chat-Kontext",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "Session-ID"},
            },
            "required": ["session_id"],
        },
    },
    {
        "name": "ollama_clear_context",
        "description": "Löscht gespeicherten Chat-Kontext",
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "Session-ID"},
            },
            "required": ["session_id"],
        },
    },
    {
        "name": "ollama_batch_generate",
        "description": "Generiert Text für mehrere Prompts gleichzeitig",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Modellname"},
                "prompts": {"type": "array", "items": {"type": "string"}, "description": "Array von Prompts"},
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["model", "prompts"],
        },
    },
    {
        "name": "ollama_compare_models",
        "description": "Vergleicht Ausgaben verschiedener Modelle für denselben Prompt",
        "inputSchema": {
            "type": "object",
            "properties": {
                "models": {"type": "array", "items": {"type": "string"}, "description": "Array von Modellnamen"},
                "prompt": {"type": "string", "description": "Vergleichs-Prompt"},
                "options": {"type": "object", "description": "Modell-Optionen"},
            },
            "required": ["models", "prompt"],
        },
    },
]


@app.get("/")
async def root():
    """Root-Endpunkt."""
    return {
        "name": "Ollama MCP Server",
        "version": "0.1.0",
        "status": "running",
        "tools_count": len(TOOLS),
    }


@app.get("/health")
async def health():
    """Health-Check Endpunkt."""
    if tool_handler:
        result = await tool_handler._check_health()
        return result
    return {"status": "unhealthy", "message": "Server nicht initialisiert"}


@app.post("/mcp/tools/list")
async def list_tools():
    """Listet alle verfügbaren Tools auf."""
    return {"tools": TOOLS}


@app.post("/mcp/tools/call")
async def call_tool(request: Dict[str, Any]):
    """Führt ein Tool aus."""
    tool_name = request.get("name")
    arguments = request.get("arguments", {})

    if not tool_name:
        raise HTTPException(status_code=400, detail="Tool-Name ist erforderlich")

    if not tool_handler:
        raise HTTPException(status_code=500, detail="Tool-Handler nicht initialisiert")

    try:
        result = await tool_handler.handle_tool_call(tool_name, arguments)
        return {"result": result}
    except Exception as e:
        logger.error(f"Fehler bei Tool-Aufruf {tool_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# JSON-RPC 2.0 Support
@app.post("/rpc")
async def json_rpc(request: Request):
    """JSON-RPC 2.0 Endpunkt."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Ungültiges JSON")

    # JSON-RPC 2.0 Request
    request_id = body.get("id")
    method = body.get("method")
    params = body.get("params", {})

    try:
        if method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            if not tool_handler:
                raise HTTPException(status_code=500, detail="Tool-Handler nicht initialisiert")
            tool_result = await tool_handler.handle_tool_call(tool_name, arguments)
            result = {"result": tool_result}
        else:
            raise HTTPException(status_code=400, detail=f"Unbekannte Methode: {method}")

        # JSON-RPC 2.0 Response
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fehler bei JSON-RPC: {e}", exc_info=True)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": str(e),
            },
        }


def main():
    """Hauptfunktion zum Starten des Servers."""
    config = get_config()
    logger.info(f"Starte MCP Server auf {config.mcp_host}:{config.mcp_port}")
    run(
        app,
        host=config.mcp_host,
        port=config.mcp_port,
        log_level=config.log_level.lower(),
    )


if __name__ == "__main__":
    main()

