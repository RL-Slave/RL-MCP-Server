# Plan: MCP Server für Ollama (Python)

## Übersicht

Dieser Plan beschreibt die Entwicklung eines Model Context Protocol (MCP) Servers in Python, der mit Ollama integriert werden kann. Der MCP Server stellt **28 vollständige Tools** bereit, die von Ollama-Modellen genutzt werden können.

### 📊 Plan-Statistik

- **Total Tools**: 28
- **Kern-Tools** (Hoch-Priorität): 8
- **Erweiterte Tools** (Mittel-Priorität): 12
- **Utility-Tools** (Niedrig-Priorität): 8
- **Tool-Kategorien**: 11
- **Geschätzte Implementierungszeit**: 6 Wochen (bei Vollzeit-Entwicklung)

### 🎯 Hauptfunktionen

- ✅ Vollständige Ollama API-Integration
- ✅ 28 spezialisierte Tools für alle Ollama-Funktionen
- ✅ Streaming-Unterstützung für Chat und Generation
- ✅ Modell-Management (Pull, Delete, Copy, Create, Update)
- ✅ Embedding-Generierung (Single & Batch)
- ✅ Context-Management für Multi-Turn Conversations
- ✅ Batch-Operationen für effiziente Verarbeitung
- ✅ System-Monitoring und Health-Checks

### 🌐 Netzwerk-Konfiguration

- **Server-Host**: `0.0.0.0` (bindet an alle Netzwerkinterfaces)
- **Server-Port**: `4838` (Standard-Port)
- **Zugriff**: Lokal und Remote über TCP/IP

## Projektstruktur

```
RL-MCP Server/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py              # Haupt-Server-Implementierung
│       ├── client.py               # Ollama API Client
│       ├── config.py               # Konfigurationsmanagement
│       ├── handlers.py             # Request-Handler
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── model_management.py    # Tools 1-6: Modell-Verwaltung
│       │   ├── text_generation.py     # Tools 7-8: Text-Generierung
│       │   ├── chat.py                # Tools 9-10: Chat-Funktionen
│       │   ├── embeddings.py          # Tools 11, 14: Embeddings
│       │   ├── processes.py           # Tool 12: Prozess-Management
│       │   ├── advanced.py            # Tools 13, 15-16: Erweiterte Funktionen
│       │   ├── system.py              # Tools 17-20: System & Monitoring
│       │   ├── batch.py               # Tools 21-22: Batch-Operationen
│       │   ├── utilities.py           # Tools 23-25: Utility-Funktionen
│       │   └── context.py             # Tools 26-28: Kontext-Management
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── validation.py          # Parameter-Validierung
│       │   ├── formatting.py          # Response-Formatierung
│       │   └── session.py             # Session-Management
│       └── exceptions.py              # Custom Exceptions
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_client.py
│   ├── test_tools/
│   │   ├── __init__.py
│   │   ├── test_model_management.py
│   │   ├── test_text_generation.py
│   │   ├── test_chat.py
│   │   └── test_embeddings.py
│   └── fixtures/
│       └── mock_ollama_responses.json
├── docs/
│   ├── api_reference.md
│   ├── tool_reference.md
│   └── examples.md
├── requirements.txt                  # Python-Abhängigkeiten
├── requirements-dev.txt              # Dev-Dependencies
├── pyproject.toml                    # Projekt-Konfiguration
├── README.md                         # Dokumentation
├── .env.example                      # Beispiel-Umgebungsvariablen
├── .gitignore
└── PLAN.md                           # Dieser Plan
```

## Tool-Übersichtstabelle

| # | Tool-Name | Kategorie | API-Endpoint | Priorität | Status |
|---|-----------|-----------|--------------|-----------|--------|
| 1 | ollama_list_models | Modell-Verwaltung | GET /api/tags | Hoch | ⬜ |
| 2 | ollama_show_model | Modell-Verwaltung | POST /api/show | Hoch | ⬜ |
| 3 | ollama_pull_model | Modell-Verwaltung | POST /api/pull | Hoch | ⬜ |
| 4 | ollama_delete_model | Modell-Verwaltung | DELETE /api/delete | Mittel | ⬜ |
| 5 | ollama_copy_model | Modell-Verwaltung | POST /api/copy | Mittel | ⬜ |
| 6 | ollama_create_model | Modell-Verwaltung | POST /api/create | Mittel | ⬜ |
| 7 | ollama_generate | Text-Generierung | POST /api/generate | Hoch | ⬜ |
| 8 | ollama_generate_stream | Text-Generierung | POST /api/generate | Hoch | ⬜ |
| 9 | ollama_chat | Chat-Funktionen | POST /api/chat | Hoch | ⬜ |
| 10 | ollama_chat_stream | Chat-Funktionen | POST /api/chat | Hoch | ⬜ |
| 11 | ollama_embeddings | Embeddings | POST /api/embeddings | Mittel | ⬜ |
| 12 | ollama_list_processes | Laufende Prozesse | GET /api/ps | Niedrig | ⬜ |
| 13 | ollama_check_blobs | Erweitert | HEAD /api/blobs/:digest | Niedrig | ⬜ |
| 14 | ollama_create_embeddings | Embeddings | POST /api/embeddings | Mittel | ⬜ |
| 15 | ollama_update_model | Modell-Konfig | POST /api/create | Mittel | ⬜ |
| 16 | ollama_get_modelfile | Modell-Konfig | POST /api/show | Mittel | ⬜ |
| 17 | ollama_get_version | System | GET /api/version | Niedrig | ⬜ |
| 18 | ollama_check_health | System | GET / | Hoch | ⬜ |
| 19 | ollama_get_models_info | System | Custom | Mittel | ⬜ |
| 20 | ollama_cancel_request | System | Custom | Mittel | ⬜ |
| 21 | ollama_batch_generate | Batch | Custom | Niedrig | ⬜ |
| 22 | ollama_compare_models | Batch | Custom | Niedrig | ⬜ |
| 23 | ollama_validate_model | Utility | Custom | Mittel | ⬜ |
| 24 | ollama_get_model_size | Utility | Custom | Niedrig | ⬜ |
| 25 | ollama_search_models | Utility | Custom | Niedrig | ⬜ |
| 26 | ollama_save_context | Kontext | Custom | Mittel | ⬜ |
| 27 | ollama_load_context | Kontext | Custom | Mittel | ⬜ |
| 28 | ollama_clear_context | Kontext | Custom | Niedrig | ⬜ |

**Legende:**
- ⬜ = Nicht implementiert
- 🟡 = In Arbeit
- ✅ = Implementiert

**Prioritäten:**
- **Hoch**: Kernfunktionalität, sollte zuerst implementiert werden
- **Mittel**: Wichtige Features, folgen nach Kernfunktionalität
- **Niedrig**: Nice-to-have Features, können später hinzugefügt werden

## Technische Anforderungen

### 1. Abhängigkeiten

- **Python 3.10+** (empfohlen: 3.11 oder höher)
- **MCP Python SDK**: `mcp` oder `anthropic-mcp`
- **JSON-RPC**: Für die Kommunikation mit MCP-Clients
- **Pydantic**: Für Datenvalidierung
- **Python-dotenv**: Für Umgebungsvariablen

### 2. Ollama-Anforderungen

- Ollama installiert und laufend
- Mindestens ein Modell (z.B. `llama2`, `mistral`, `codellama`)
- Ollama API erreichbar (Standard: `http://localhost:11434`)

## Implementierungsplan

### Phase 1: Grundgerüst (Foundation)

1. **Projekt-Setup**
   - Python-Projekt initialisieren
   - Virtual Environment erstellen
   - `requirements.txt` und `pyproject.toml` erstellen
   - Basis-Projektstruktur anlegen

2. **MCP Server Basis-Implementierung**
   - MCP Server Klasse erstellen
   - JSON-RPC Kommunikation implementieren
   - Basis-Handler für MCP-Protokoll registrieren
   - Fehlerbehandlung implementieren

### Phase 2: Ollama-Integration

3. **Ollama-Client Integration**
   - Ollama API Client erstellen
   - Funktionen für:
     - Modell-Liste abrufen
     - Modelle herunterladen (`ollama pull`)
     - Completion/Generation
     - Chat-Completion
   - Konfiguration (Host, Port, Timeout)

4. **MCP Tools für Ollama** (28 Tools total)
   - **Phase 2a - Kernfunktionen** (Hoch-Priorität):
     - `ollama_list_models`: Liste verfügbarer Modelle
     - `ollama_show_model`: Modell-Details anzeigen
     - `ollama_pull_model`: Modell herunterladen
     - `ollama_generate`: Text generieren
     - `ollama_generate_stream`: Streaming-Generierung
     - `ollama_chat`: Chat-Kompletierung
     - `ollama_chat_stream`: Streaming-Chat
     - `ollama_check_health`: Health-Check
   
   - **Phase 2b - Erweiterte Funktionen** (Mittel-Priorität):
     - `ollama_delete_model`: Modell löschen
     - `ollama_copy_model`: Modell kopieren
     - `ollama_create_model`: Modell erstellen
     - `ollama_embeddings`: Embeddings generieren
     - `ollama_create_embeddings`: Batch-Embeddings
     - `ollama_update_model`: Modell aktualisieren
     - `ollama_get_modelfile`: Modelfile abrufen
     - `ollama_get_models_info`: Alle Modell-Infos
     - `ollama_cancel_request`: Request abbrechen
     - `ollama_validate_model`: Modell validieren
     - `ollama_save_context`: Kontext speichern
     - `ollama_load_context`: Kontext laden
   
   - **Phase 2c - Utility-Funktionen** (Niedrig-Priorität):
     - `ollama_list_processes`: Prozesse auflisten
     - `ollama_check_blobs`: Blob-Status prüfen
     - `ollama_get_version`: Version abrufen
     - `ollama_batch_generate`: Batch-Generierung
     - `ollama_compare_models`: Modelle vergleichen
     - `ollama_get_model_size`: Modell-Größe
     - `ollama_search_models`: Modelle durchsuchen
     - `ollama_clear_context`: Kontext löschen

### Phase 3: Erweiterte Features

5. **Tool-Management**
   - Dynamische Tool-Registrierung
   - Tool-Metadaten und Beschreibungen
   - Parameter-Validierung
   - Tool-Versionierung

6. **Konfiguration & Sicherheit**
   - Konfigurationsdatei-Support
   - Umgebungsvariablen für sensible Daten
   - Rate-Limiting
   - Authentifizierung (optional)

### Phase 4: Testing & Dokumentation

7. **Testing**
   - Unit-Tests für Server-Funktionen
   - Integration-Tests mit Ollama
   - Mock-Tests für API-Aufrufe
   - Test-Dokumentation

8. **Dokumentation**
   - README mit Installationsanleitung
   - API-Dokumentation
   - Beispiel-Konfigurationen
   - Verwendungsbeispiele

## Detaillierte Implementierung

### Server-Architektur

```python
# Basis-Struktur
class MCPServer:
    - __init__(host="0.0.0.0", port=4838)  # Server-Konfiguration
    - initialize()      # Server initialisieren
    - list_tools()       # Verfügbare Tools auflisten
    - call_tool()        # Tool ausführen
    - handle_request()   # JSON-RPC Requests verarbeiten
    - run()              # Server starten (bindet an 0.0.0.0:4838)
    - stop()             # Server stoppen
    
# Konfiguration
class Config:
    - host: str = "0.0.0.0"      # Standard: Alle Interfaces
    - port: int = 4838            # Standard-Port
    - ollama_host: str = "localhost"
    - ollama_port: int = 11434
    - timeout: int = 60
```

### Tools-Implementierung

Jedes Tool sollte folgende Struktur haben:
- **Name**: Eindeutiger Tool-Name
- **Description**: Beschreibung für das LLM
- **Parameters**: Schema für Input-Parameter
- **Handler**: Funktion zur Ausführung

### Vollständige Tool-Liste

#### Kategorie 1: Modell-Verwaltung

1. **ollama_list_models** (GET /api/tags)
   - Beschreibung: "Listet alle verfügbaren Ollama-Modelle mit Details auf"
   - Parameter: Keine
   - Rückgabe: Liste von Modellen mit Namen, Größe, Modifizierungsdatum
   - Details: Zeigt alle lokalen Modelle mit Metadaten

2. **ollama_show_model** (POST /api/show)
   - Beschreibung: "Zeigt detaillierte Informationen zu einem spezifischen Modell an"
   - Parameter:
     - `model`: Modellname (string, required)
   - Rückgabe: Modell-Details (Modelfile, Parameter, Template, etc.)
   - Details: Zeigt Modelfile, Parameter, System-Template, Prompt-Template

3. **ollama_pull_model** (POST /api/pull)
   - Beschreibung: "Lädt ein Modell aus dem Ollama-Registry herunter"
   - Parameter:
     - `model`: Modellname (string, required)
     - `insecure`: Unsichere Registry verwenden (bool, optional)
   - Rückgabe: Download-Fortschritt und Status
   - Details: Unterstützt Streaming von Download-Status

4. **ollama_delete_model** (DELETE /api/delete)
   - Beschreibung: "Löscht ein Modell vom lokalen System"
   - Parameter:
     - `model`: Modellname (string, required)
   - Rückgabe: Lösch-Status
   - Details: Entfernt Modell und freigegebenen Speicher

5. **ollama_copy_model** (POST /api/copy)
   - Beschreibung: "Kopiert ein Modell unter neuem Namen"
   - Parameter:
     - `source`: Quell-Modellname (string, required)
     - `destination`: Ziel-Modellname (string, required)
   - Rückgabe: Kopier-Status
   - Details: Erstellt eine Kopie eines Modells mit neuem Namen

6. **ollama_create_model** (POST /api/create)
   - Beschreibung: "Erstellt ein neues Modell aus einer Modelfile"
   - Parameter:
     - `model`: Modellname (string, required)
     - `modelfile`: Modelfile-Inhalt (string, required)
     - `stream`: Streaming aktivieren (bool, optional)
   - Rückgabe: Erstellungs-Status
   - Details: Erstellt Custom-Modelle aus Modelfile-Definitionen

#### Kategorie 2: Text-Generierung

7. **ollama_generate** (POST /api/generate)
   - Beschreibung: "Generiert Text mit einem Ollama-Modell basierend auf einem Prompt"
   - Parameter:
     - `model`: Modellname (string, required)
     - `prompt`: Eingabe-Prompt (string, required)
     - `system`: System-Prompt (string, optional)
     - `template`: Prompt-Template (string, optional)
     - `context`: Kontext-Array (array, optional)
     - `stream`: Streaming aktivieren (bool, optional)
     - `options`: Modell-Optionen (object, optional):
       - `temperature`: Temperatur für Sampling (float, 0.0-1.0)
       - `top_p`: Top-p Sampling (float)
       - `top_k`: Top-k Sampling (int)
       - `repeat_penalty`: Wiederholungs-Strafe (float)
       - `seed`: Zufalls-Seed (int)
       - `num_predict`: Maximale Token-Anzahl (int)
       - `stop`: Stop-Sequenzen (array)
       - `num_ctx`: Kontext-Window-Größe (int)
       - `num_parts`: Anzahl Teile (int)
       - `num_thread`: Anzahl Threads (int)
       - `repeat_last_n`: Anzahl zu betrachtende Token für Repeat-Penalty (int)
       - `use_mmap`: Memory-Mapping verwenden (bool)
       - `use_mlock`: Memory-Locking verwenden (bool)
       - `num_gpu`: Anzahl GPU-Layer (int)
       - `main_gpu`: Haupt-GPU (int)
       - `low_vram`: Niedriges VRAM verwenden (bool)
       - `f16_kv`: F16 für KV-Cache (bool)
       - `vocab_only`: Nur Vokabular laden (bool)
       - `use_mmap`: Memory-Mapping verwenden (bool)
       - `embedding_only`: Nur Embeddings generieren (bool)
   - Rückgabe: Generierter Text mit Kontext für weitere Anfragen
   - Details: Basis-Generierung mit vollständiger Konfiguration

8. **ollama_generate_stream** (POST /api/generate - stream)
   - Beschreibung: "Generiert Text im Streaming-Modus (Token für Token)"
   - Parameter: Wie `ollama_generate`, aber `stream=true`
   - Rückgabe: Streaming Response (jedes Token einzeln)
   - Details: Real-time Text-Generierung

#### Kategorie 3: Chat-Funktionen

9. **ollama_chat** (POST /api/chat)
   - Beschreibung: "Führt eine Chat-Konversation mit einem Modell"
   - Parameter:
     - `model`: Modellname (string, required)
     - `messages`: Array von Chat-Nachrichten (array, required):
       - `role`: "system", "user", "assistant" (string, required)
       - `content`: Nachrichteninhalt (string, required)
     - `stream`: Streaming aktivieren (bool, optional)
     - `options`: Modell-Optionen (object, optional) - siehe `ollama_generate`
   - Rückgabe: Chat-Antwort mit Kontext
   - Details: Multi-Turn Conversations mit Context-Management

10. **ollama_chat_stream** (POST /api/chat - stream)
    - Beschreibung: "Führt Chat im Streaming-Modus durch"
    - Parameter: Wie `ollama_chat`, aber `stream=true`
    - Rückgabe: Streaming Chat-Response
    - Details: Real-time Chat-Antworten

#### Kategorie 4: Embeddings

11. **ollama_embeddings** (POST /api/embeddings)
    - Beschreibung: "Generiert Embedding-Vektoren für einen gegebenen Text"
    - Parameter:
      - `model`: Modellname (string, required)
      - `prompt`: Text für Embedding (string, required)
      - `options`: Modell-Optionen (object, optional)
    - Rückgabe: Embedding-Vektor (Array von Floats)
    - Details: Erstellt numerische Repräsentationen für Vektor-Suche

#### Kategorie 5: Laufende Prozesse

12. **ollama_list_processes** (GET /api/ps)
    - Beschreibung: "Listet alle laufenden Modell-Inferenz-Prozesse auf"
    - Parameter: Keine
    - Rückgabe: Liste von Prozessen mit Details:
      - Modellname
      - PID
      - GPU-Speicher-Nutzung
      - Prompt-Evaluierungszeit
      - Verbleibende Zeit
    - Details: Monitoring von aktiven Generierungen

#### Kategorie 6: Erweiterte Funktionen

13. **ollama_check_blobs** (HEAD /api/blobs/:digest)
    - Beschreibung: "Prüft ob ein Blob (Modell-Teil) vorhanden ist"
    - Parameter:
      - `digest`: Blob-Digest (string, required)
    - Rückgabe: Existenz-Status des Blobs
    - Details: Interne Modell-Verwaltung

14. **ollama_create_embeddings** (POST /api/embeddings)
    - Beschreibung: "Erstellt Embeddings für mehrere Texte gleichzeitig"
    - Parameter:
      - `model`: Modellname (string, required)
      - `prompts`: Array von Texten (array, required)
      - `options`: Modell-Optionen (object, optional)
    - Rückgabe: Array von Embedding-Vektoren
    - Details: Batch-Embedding-Generierung

#### Kategorie 7: Modell-Konfiguration & Templates

15. **ollama_update_model** (POST /api/create)
    - Beschreibung: "Aktualisiert ein bestehendes Modell mit neuer Modelfile"
    - Parameter:
      - `model`: Modellname (string, required)
      - `modelfile`: Neue Modelfile-Definition (string, required)
      - `overwrite`: Überschreiben erlauben (bool, optional)
    - Rückgabe: Update-Status
    - Details: Ändert Modell-Parameter, Templates, etc.

16. **ollama_get_modelfile** (POST /api/show)
    - Beschreibung: "Ruft die Modelfile-Konfiguration eines Modells ab"
    - Parameter:
      - `model`: Modellname (string, required)
    - Rückgabe: Modelfile-Inhalt als String
    - Details: Liest komplette Modell-Definition

#### Kategorie 8: System & Monitoring

17. **ollama_get_version** (GET /api/version)
    - Beschreibung: "Ruft die Ollama-Server-Version ab"
    - Parameter: Keine
    - Rückgabe: Versionsinformationen
    - Details: System-Informationen

18. **ollama_check_health** (GET /api/tags oder /)
    - Beschreibung: "Prüft ob Ollama-Server erreichbar und funktionsfähig ist"
    - Parameter: Keine
    - Rückgabe: Health-Status
    - Details: Health-Check für Monitoring

19. **ollama_get_models_info**
    - Beschreibung: "Ruft detaillierte Informationen über alle Modelle ab"
    - Parameter: Keine
    - Rückgabe: Array mit vollständigen Modell-Informationen
    - Details: Kombiniert list und show für alle Modelle

20. **ollama_cancel_request** (Custom)
    - Beschreibung: "Bricht eine laufende Generierung ab"
    - Parameter:
      - `request_id`: Request-ID (string, optional)
    - Rückgabe: Abbruch-Status
    - Details: Stoppt laufende Inferenz-Prozesse

#### Kategorie 9: Batch-Operationen

21. **ollama_batch_generate**
    - Beschreibung: "Generiert Text für mehrere Prompts gleichzeitig"
    - Parameter:
      - `model`: Modellname (string, required)
      - `prompts`: Array von Prompts (array, required)
      - `options`: Modell-Optionen (object, optional)
    - Rückgabe: Array von Generierungs-Ergebnissen
    - Details: Effiziente Batch-Verarbeitung

22. **ollama_compare_models**
    - Beschreibung: "Vergleicht Ausgaben verschiedener Modelle für denselben Prompt"
    - Parameter:
      - `models`: Array von Modellnamen (array, required)
      - `prompt`: Vergleichs-Prompt (string, required)
      - `options`: Modell-Optionen (object, optional)
    - Rückgabe: Vergleichs-Ergebnisse
    - Details: Model-Benchmarking

#### Kategorie 10: Utility-Funktionen

23. **ollama_validate_model**
    - Beschreibung: "Validiert ob ein Modell korrekt installiert und funktionsfähig ist"
    - Parameter:
      - `model`: Modellname (string, required)
    - Rückgabe: Validierungs-Ergebnis mit Details
    - Details: Modell-Integritätsprüfung

24. **ollama_get_model_size**
    - Beschreibung: "Ruft die Speichergröße eines Modells ab"
    - Parameter:
      - `model`: Modellname (string, required)
    - Rückgabe: Größe in Bytes und lesbarem Format
    - Details: Speicher-Management

25. **ollama_search_models**
    - Beschreibung: "Durchsucht verfügbare Modelle nach Namen oder Tags"
    - Parameter:
      - `query`: Suchbegriff (string, required)
      - `remote`: Auch Remote-Registry durchsuchen (bool, optional)
    - Rückgabe: Gefundene Modelle
    - Details: Modell-Discovery

#### Kategorie 11: Kontext-Management

26. **ollama_save_context**
    - Beschreibung: "Speichert Chat-Kontext für spätere Verwendung"
    - Parameter:
      - `session_id`: Session-ID (string, required)
      - `messages`: Chat-Messages (array, required)
    - Rückgabe: Speicher-Status
    - Details: Session-Persistenz

27. **ollama_load_context**
    - Beschreibung: "Lädt gespeicherten Chat-Kontext"
    - Parameter:
      - `session_id`: Session-ID (string, required)
    - Rückgabe: Gespeicherte Messages
    - Details: Session-Wiederherstellung

28. **ollama_clear_context**
    - Beschreibung: "Löscht gespeicherten Chat-Kontext"
    - Parameter:
      - `session_id`: Session-ID (string, required)
    - Rückgabe: Lösch-Status
    - Details: Session-Cleanup

## Konfiguration

### Server-Netzwerk-Konfiguration

Der MCP Server läuft standardmäßig auf:
- **Host**: `0.0.0.0` (alle Netzwerkinterfaces)
- **Port**: `4838` (Standard-Port)

Diese Konfiguration ermöglicht:
- Zugriff von allen Netzwerkinterfaces (nicht nur localhost)
- Remote-Zugriff von anderen Rechnern im Netzwerk
- Standardisierter Port für einfache Firewall-Konfiguration

### Umgebungsvariablen (.env)

```
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

### MCP Server Konfiguration (für MCP Clients)

```json
{
  "mcpServers": {
    "ollama-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "MCP_HOST": "0.0.0.0",
        "MCP_PORT": "4838",
        "OLLAMA_HOST": "localhost",
        "OLLAMA_PORT": "11434"
      }
    }
  }
}
```

### Beispiel: Server starten

```python
# server.py
from mcp_server.config import Config

config = Config()
config.host = "0.0.0.0"
config.port = 4838

# Server starten
server = MCPServer(config)
server.run()
```

### Firewall-Konfiguration

Für den Zugriff von außen muss Port 4838 geöffnet werden:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 4838/tcp

# firewalld (RHEL/CentOS)
sudo firewall-cmd --add-port=4838/tcp --permanent
sudo firewall-cmd --reload

# iptables (generisch)
sudo iptables -A INPUT -p tcp --dport 4838 -j ACCEPT
```

## Abhängigkeitsliste (requirements.txt)

```
# MCP Protocol
mcp>=0.1.0

# HTTP Client für Ollama API
httpx>=0.25.0
aiohttp>=3.9.0

# Datenvalidierung
pydantic>=2.0.0

# Konfiguration
python-dotenv>=1.0.0

# Logging
structlog>=23.0.0

# Testing (dev)
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-mock>=3.12.0
```

## Implementierungsreihenfolge

### Schritt 1: Basis-Setup
- [ ] Projekt-Struktur erstellen
- [ ] `requirements.txt` erstellen
- [ ] Virtual Environment einrichten
- [ ] Basis-Importe und Struktur

### Schritt 2: Ollama Client
- [ ] Ollama API Client Klasse
- [ ] HTTP-Client für Ollama API
- [ ] Basis-Funktionen (list, generate, chat)

### Schritt 3: MCP Server Basis
- [ ] MCP Server Klasse
- [ ] JSON-RPC Handler
- [ ] Basis-Protokoll-Implementierung

### Schritt 4: Kern-Tools implementieren (Phase 2a)
- [ ] ollama_check_health - Health-Check
- [ ] ollama_list_models - Modell-Liste
- [ ] ollama_show_model - Modell-Details
- [ ] ollama_pull_model - Modell-Download
- [ ] ollama_generate - Text-Generierung
- [ ] ollama_generate_stream - Streaming-Generierung
- [ ] ollama_chat - Chat-Kompletierung
- [ ] ollama_chat_stream - Streaming-Chat

### Schritt 5: Erweiterte Tools (Phase 2b)
- [ ] ollama_delete_model - Modell löschen
- [ ] ollama_copy_model - Modell kopieren
- [ ] ollama_create_model - Modell erstellen
- [ ] ollama_embeddings - Embeddings
- [ ] ollama_create_embeddings - Batch-Embeddings
- [ ] ollama_update_model - Modell aktualisieren
- [ ] ollama_get_modelfile - Modelfile abrufen
- [ ] ollama_get_models_info - Alle Infos
- [ ] ollama_cancel_request - Request abbrechen
- [ ] ollama_validate_model - Validierung
- [ ] ollama_save_context - Kontext speichern
- [ ] ollama_load_context - Kontext laden

### Schritt 6: Utility-Tools (Phase 2c)
- [ ] ollama_list_processes - Prozesse
- [ ] ollama_check_blobs - Blob-Check
- [ ] ollama_get_version - Version
- [ ] ollama_batch_generate - Batch
- [ ] ollama_compare_models - Vergleich
- [ ] ollama_get_model_size - Größe
- [ ] ollama_search_models - Suche
- [ ] ollama_clear_context - Kontext löschen

### Schritt 7: Tool-Integration
- [ ] Tool-Registrierungssystem
- [ ] Tool-Metadaten-Verwaltung
- [ ] Parameter-Validierung mit Pydantic
- [ ] Error-Handling für alle Tools
- [ ] Response-Formatierung

### Schritt 8: Konfiguration
- [ ] Config-Management-System
- [ ] Environment-Variables-Support
- [ ] Logging-Setup (strukturiert)
- [ ] Rate-Limiting-Konfiguration
- [ ] Session-Management-Konfiguration

### Schritt 9: Testing
- [ ] Unit-Tests für alle Tools
- [ ] Integration-Tests mit Ollama
- [ ] Mock-Tests für Ollama API
- [ ] Test-Fixuren erstellen
- [ ] CI/CD Pipeline (optional)

### Schritt 10: Dokumentation
- [ ] README.md mit vollständiger Anleitung
- [ ] API-Referenz-Dokumentation
- [ ] Tool-Referenz für jedes Tool
- [ ] Code-Kommentare (Docstrings)
- [ ] Beispiel-Konfigurationen
- [ ] Use-Case-Beispiele

## Implementierungsstrategie für alle 28 Tools

### Phase 2a: Kern-Tools (8 Tools) - Woche 1-2
Diese Tools sind essentiell für die Grundfunktionalität:
1. ✅ ollama_check_health - Als erstes implementieren (Verbindungstest)
2. ✅ ollama_list_models - Basis-Modell-Information
3. ✅ ollama_show_model - Erweiterte Modell-Info
4. ✅ ollama_pull_model - Modell-Management
5. ✅ ollama_generate - Hauptfunktionalität
6. ✅ ollama_generate_stream - Streaming-Variante
7. ✅ ollama_chat - Chat-Funktionalität
8. ✅ ollama_chat_stream - Streaming-Chat

### Phase 2b: Erweiterte Tools (12 Tools) - Woche 3-4
Wichtige Features für Produktivnutzung:
9. ✅ ollama_delete_model
10. ✅ ollama_copy_model
11. ✅ ollama_create_model
12. ✅ ollama_embeddings
13. ✅ ollama_create_embeddings
14. ✅ ollama_update_model
15. ✅ ollama_get_modelfile
16. ✅ ollama_get_models_info
17. ✅ ollama_cancel_request
18. ✅ ollama_validate_model
19. ✅ ollama_save_context
20. ✅ ollama_load_context

### Phase 2c: Utility-Tools (8 Tools) - Woche 5-6
Nice-to-have Features:
21. ✅ ollama_list_processes
22. ✅ ollama_check_blobs
23. ✅ ollama_get_version
24. ✅ ollama_batch_generate
25. ✅ ollama_compare_models
26. ✅ ollama_get_model_size
27. ✅ ollama_search_models
28. ✅ ollama_clear_context

### Tool-Implementierungs-Template

Jedes Tool sollte diesem Schema folgen:

```python
@tool_registry.register("ollama_tool_name")
async def ollama_tool_name(params: ToolParams) -> ToolResult:
    """
    Tool-Beschreibung für das LLM
    
    Args:
        params: Validierte Tool-Parameter
        
    Returns:
        ToolResult mit Ergebnis oder Fehler
    """
    try:
        # 1. Parameter-Validierung
        validated = validate_params(params, ToolSchema)
        
        # 2. Ollama API Aufruf
        result = await ollama_client.call_api(...)
        
        # 3. Response-Formatierung
        return ToolResult(
            success=True,
            data=format_response(result),
            metadata={...}
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=str(e),
            error_code="TOOL_ERROR"
        )
```

## Nächste Schritte

1. **Projekt initialisieren**: Struktur erstellen und Dependencies installieren
2. **Ollama-Verbindung testen**: Einfachen Client erstellen und testen
3. **MCP Server Basis**: Minimalen MCP Server implementieren
4. **Phase 2a - Kern-Tools**: Alle 8 Kern-Tools implementieren
5. **Phase 2b - Erweiterte Tools**: 12 erweiterte Tools hinzufügen
6. **Phase 2c - Utility-Tools**: 8 Utility-Tools abschließen
7. **Testing & Dokumentation**: Vollständige Test-Suite und Docs

## Ressourcen

- [MCP Specification](https://modelcontextprotocol.io/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Python MCP Examples](https://github.com/modelcontextprotocol/servers)

## Erweiterte Ideen (Optional)

- Model-Management Tools (delete, info)
- Multi-Model Support
- Streaming-Unterstützung
- Context-Management
- Prompt-Templates
- Batch-Processing
- Model-Fine-Tuning Support
- Performance-Monitoring

