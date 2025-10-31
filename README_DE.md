# Ollama MCP Server

Ein vollständiger Model Context Protocol (MCP) Server für Ollama mit **28 Tools**, der es ermöglicht, Ollama-Modelle über das MCP-Protokoll zu nutzen.

## Features

- ✅ **28 vollständige Tools** für alle Ollama-Funktionen
- ✅ **Streaming-Unterstützung** für Chat und Text-Generierung
- ✅ **Modell-Management** (Pull, Delete, Copy, Create, Update)
- ✅ **Embedding-Generierung** (Single & Batch)
- ✅ **Context-Management** für Multi-Turn Conversations
- ✅ **Batch-Operationen** für effiziente Verarbeitung
- ✅ **System-Monitoring** und Health-Checks
- ✅ **Remote-Zugriff** über 0.0.0.0:4838

## Installation

### Voraussetzungen

- Python 3.10 oder höher
- Ollama installiert und laufend
- Mindestens ein Ollama-Modell (z.B. `ollama pull llama2`)

### Installation

1. **Repository klonen oder Dateien extrahieren**

2. **Virtual Environment erstellen**:
```bash
python -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

3. **Abhängigkeiten installieren**:
```bash
pip install -r requirements.txt
```

4. **Konfiguration anpassen** (optional):
```bash
cp env.example .env
# .env bearbeiten falls nötig
```

## Verwendung

### Server starten

```bash
# Direkt
python -m mcp_server.server

# Oder mit Start-Skript
./start.sh

# Oder mit uvicorn
uvicorn mcp_server.server:app --host 0.0.0.0 --port 4838
```

Der Server läuft standardmäßig auf **0.0.0.0:4838**.

### API-Endpunkte

#### Health-Check
```bash
curl http://localhost:4838/health
```

#### Tools auflisten
```bash
curl -X POST http://localhost:4838/mcp/tools/list
```

#### Tool aufrufen
```bash
curl -X POST http://localhost:4838/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ollama_list_models",
    "arguments": {}
  }'
```

#### JSON-RPC 2.0
```bash
curl -X POST http://localhost:4838/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## Verfügbare Tools

### Modell-Verwaltung
- `ollama_list_models` - Listet alle Modelle auf
- `ollama_show_model` - Zeigt Modell-Details
- `ollama_pull_model` - Lädt Modell herunter
- `ollama_delete_model` - Löscht Modell
- `ollama_copy_model` - Kopiert Modell
- `ollama_create_model` - Erstellt Modell aus Modelfile

### Text-Generierung
- `ollama_generate` - Generiert Text
- `ollama_generate_stream` - Streaming-Generierung

### Chat-Funktionen
- `ollama_chat` - Chat-Kompletierung
- `ollama_chat_stream` - Streaming-Chat

### Embeddings
- `ollama_embeddings` - Embeddings generieren
- `ollama_create_embeddings` - Batch-Embeddings

### System & Monitoring
- `ollama_check_health` - Health-Check
- `ollama_get_version` - Ollama-Version
- `ollama_list_processes` - Laufende Prozesse
- `ollama_get_models_info` - Alle Modell-Infos

### Weitere Tools
- `ollama_update_model` - Modell aktualisieren
- `ollama_get_modelfile` - Modelfile abrufen
- `ollama_validate_model` - Modell validieren
- `ollama_get_model_size` - Modell-Größe
- `ollama_search_models` - Modelle durchsuchen
- `ollama_check_blobs` - Blob-Status
- `ollama_save_context` - Kontext speichern
- `ollama_load_context` - Kontext laden
- `ollama_clear_context` - Kontext löschen
- `ollama_batch_generate` - Batch-Generierung
- `ollama_compare_models` - Modelle vergleichen

## Konfiguration

### Umgebungsvariablen

Erstellen Sie eine `.env` Datei:

```env
# MCP Server Konfiguration
MCP_HOST=0.0.0.0
MCP_PORT=4838

# Ollama API Konfiguration
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_TIMEOUT=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Firewall-Konfiguration

Für Remote-Zugriff muss Port 4838 geöffnet werden:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 4838/tcp

# firewalld (RHEL/CentOS)
sudo firewall-cmd --add-port=4838/tcp --permanent
sudo firewall-cmd --reload
```

## Beispiel-Verwendung

### Python Client

```python
import httpx

# Tool aufrufen
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:4838/mcp/tools/call",
        json={
            "name": "ollama_generate",
            "arguments": {
                "model": "llama2",
                "prompt": "Erkläre mir Python in einem Satz.",
            }
        }
    )
    print(response.json())
```

### cURL Beispiele

#### Text generieren
```bash
curl -X POST http://localhost:4838/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ollama_generate",
    "arguments": {
      "model": "llama2",
      "prompt": "Was ist Machine Learning?"
    }
  }'
```

#### Chat
```bash
curl -X POST http://localhost:4838/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ollama_chat",
    "arguments": {
      "model": "llama2",
      "messages": [
        {"role": "user", "content": "Hallo!"}
      ]
    }
  }'
```

## Projektstruktur

```
RL-MCP Server/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py          # Haupt-Server
│       ├── client.py          # Ollama API Client
│       ├── config.py          # Konfiguration
│       ├── handlers.py        # Tool-Handler
│       ├── exceptions.py      # Exceptions
│       └── utils/             # Utilities
├── tests/                      # Tests
├── examples/                   # Beispiele
├── requirements.txt           # Dependencies
├── pyproject.toml            # Projekt-Konfiguration
├── README_DE.md              # Diese Datei
├── README_EN.md              # Englische Version
└── LICENSE                   # Lizenz
```

## Entwicklung

### Tests ausführen

```bash
pytest
```

### Code-Formatierung

```bash
black src/
ruff check src/
```

## Lizenz

Siehe [LICENSE](LICENSE) Datei.

## Autor

**Robin Oliver Lucas**
- Website: https://rl-dev.de
- Email: robin@rl-dev.de

## Unterstützung

Bei Fragen oder Problemen erstellen Sie bitte ein Issue oder kontaktieren Sie den Autor.

## Weitere Informationen

- [Installationsanleitung](INSTALL.md)
- [Plan & Architektur](PLAN.md)
- [Checkliste](CHECKLIST.md)

