"""Session-Management für Kontext-Speicherung."""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp_server.config import get_config
from mcp_server.exceptions import MCPError


class SessionManager:
    """Verwaltet Sessions für Chat-Kontext."""

    def __init__(self, config=None):
        """Initialisiert den Session Manager."""
        self.config = config or get_config()
        self.storage_path = Path(self.config.session_storage_path)
        self.ttl = self.config.session_ttl
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_session_path(self, session_id: str) -> Path:
        """Gibt den Pfad für eine Session zurück."""
        return self.storage_path / f"{session_id}.json"

    def save_context(self, session_id: str, messages: List[Dict[str, Any]]) -> bool:
        """Speichert Chat-Kontext für eine Session."""
        try:
            session_data = {
                "session_id": session_id,
                "messages": messages,
                "created_at": time.time(),
                "updated_at": time.time(),
            }
            session_path = self._get_session_path(session_id)
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2)
            return True
        except Exception as e:
            raise MCPError(f"Fehler beim Speichern der Session: {e}")

    def load_context(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        """Lädt Chat-Kontext für eine Session."""
        try:
            session_path = self._get_session_path(session_id)
            if not session_path.exists():
                return None

            with open(session_path, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            # Prüfe TTL
            if time.time() - session_data.get("updated_at", 0) > self.ttl:
                self.clear_context(session_id)
                return None

            return session_data.get("messages", [])
        except Exception as e:
            raise MCPError(f"Fehler beim Laden der Session: {e}")

    def clear_context(self, session_id: str) -> bool:
        """Löscht Chat-Kontext für eine Session."""
        try:
            session_path = self._get_session_path(session_id)
            if session_path.exists():
                session_path.unlink()
            return True
        except Exception as e:
            raise MCPError(f"Fehler beim Löschen der Session: {e}")

    def update_context(self, session_id: str, message: Dict[str, Any]) -> bool:
        """Aktualisiert den Kontext mit einer neuen Nachricht."""
        messages = self.load_context(session_id) or []
        messages.append(message)
        return self.save_context(session_id, messages)

