#!/bin/bash
# Start-Skript für MCP Server

echo "Starte Ollama MCP Server..."

# Prüfe ob Virtual Environment aktiviert ist
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warnung: Virtual Environment nicht aktiviert!"
    echo "Führe aus: source venv/bin/activate"
    read -p "Trotzdem fortfahren? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Starte Server
python -m mcp_server.server

