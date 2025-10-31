# Installationsanleitung

## Schnellstart

### 1. Voraussetzungen prüfen

```bash
# Python Version prüfen (muss 3.10+ sein)
python3 --version

# Ollama installieren (falls noch nicht installiert)
# Siehe: https://ollama.ai

# Ollama starten und Modell herunterladen
ollama serve  # In einem Terminal
ollama pull llama2  # In einem anderen Terminal
```

### 2. Projekt-Setup

```bash
# In das Projektverzeichnis wechseln
cd "/media/robin/sdc1/Any/RL-MCP Server"

# Virtual Environment erstellen
python3 -m venv venv

# Virtual Environment aktivieren
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Konfiguration (optional)

```bash
# .env Datei erstellen (falls gewünscht)
cp env.example .env

# .env bearbeiten falls nötig
nano .env  # oder vim/editor Ihrer Wahl
```

### 4. Server starten

**Option 1: Mit Python direkt**
```bash
python -m mcp_server.server
```

**Option 2: Mit Start-Skript**
```bash
./start.sh
```

**Option 3: Mit uvicorn**
```bash
uvicorn mcp_server.server:app --host 0.0.0.0 --port 4838
```

### 5. Server testen

**Health-Check:**
```bash
curl http://localhost:4838/health
```

**Tools auflisten:**
```bash
curl -X POST http://localhost:4838/mcp/tools/list
```

**Beispiel-Client ausführen:**
```bash
python examples/client_example.py
```

## Troubleshooting

### Problem: Port 4838 bereits belegt
```bash
# Port prüfen
lsof -i :4838  # Linux/Mac
netstat -ano | findstr :4838  # Windows

# Anderen Port verwenden:
export MCP_PORT=4839
python -m mcp_server.server
```

### Problem: Ollama nicht erreichbar
```bash
# Ollama Status prüfen
curl http://localhost:11434/api/tags

# Ollama neu starten falls nötig
ollama serve
```

### Problem: Module nicht gefunden
```bash
# Virtual Environment aktivieren
source venv/bin/activate

# Dependencies neu installieren
pip install -r requirements.txt
```

### Problem: Permission Denied (Linux)
```bash
# Firewall konfigurieren
sudo ufw allow 4838/tcp

# Falls nötig, mit sudo starten (nicht empfohlen)
sudo python -m mcp_server.server
```

## Systemd Service (Linux - Optional)

Für automatischen Start bei Boot:

```bash
# Service-Datei erstellen
sudo nano /etc/systemd/system/ollama-mcp-server.service
```

Inhalt:
```ini
[Unit]
Description=Ollama MCP Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/media/robin/sdc1/Any/RL-MCP Server
Environment="PATH=/media/robin/sdc1/Any/RL-MCP Server/venv/bin"
ExecStart=/media/robin/sdc1/Any/RL-MCP Server/venv/bin/python -m mcp_server.server
Restart=always

[Install]
WantedBy=multi-user.target
```

Aktivieren:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama-mcp-server
sudo systemctl start ollama-mcp-server
sudo systemctl status ollama-mcp-server
```

