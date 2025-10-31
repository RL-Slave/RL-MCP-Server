"""Konfigurationsmanagement für den MCP Server."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Konfiguration für MCP Server und Ollama."""

    # MCP Server Konfiguration
    mcp_host: str = Field(default="0.0.0.0", description="Host für MCP Server")
    mcp_port: int = Field(default=4838, description="Port für MCP Server")

    # Ollama API Konfiguration
    ollama_host: str = Field(default="localhost", description="Ollama API Host")
    ollama_port: int = Field(default=11434, description="Ollama API Port")
    ollama_timeout: int = Field(default=60, description="Ollama API Timeout in Sekunden")

    # Logging
    log_level: str = Field(default="INFO", description="Log-Level")
    log_format: str = Field(default="json", description="Log-Format (json/text)")

    # Session Management
    session_storage_path: Path = Field(
        default=Path("./sessions"), description="Pfad für Session-Speicherung"
    )
    session_ttl: int = Field(
        default=3600, description="Session TTL in Sekunden"
    )

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=False, description="Rate Limiting aktivieren")
    rate_limit_requests_per_minute: int = Field(
        default=60, description="Anfragen pro Minute"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="",  # Kein Prefix, direkte Variablennamen
    )

    @property
    def ollama_base_url(self) -> str:
        """Gibt die Basis-URL für Ollama API zurück."""
        return f"http://{self.ollama_host}:{self.ollama_port}"

    @property
    def mcp_address(self) -> tuple[str, int]:
        """Gibt die Bind-Adresse für den MCP Server zurück."""
        return (self.mcp_host, self.mcp_port)

    def __init__(self, **kwargs):
        """Initialisiert die Konfiguration."""
        # Konvertiere Umgebungsvariablen
        env_mapping = {
            "MCP_HOST": "mcp_host",
            "MCP_PORT": "mcp_port",
            "OLLAMA_HOST": "ollama_host",
            "OLLAMA_PORT": "ollama_port",
            "OLLAMA_TIMEOUT": "ollama_timeout",
            "LOG_LEVEL": "log_level",
            "LOG_FORMAT": "log_format",
            "SESSION_STORAGE_PATH": "session_storage_path",
            "SESSION_TTL": "session_ttl",
            "RATE_LIMIT_ENABLED": "rate_limit_enabled",
            "RATE_LIMIT_REQUESTS_PER_MINUTE": "rate_limit_requests_per_minute",
        }

        # Lese Umgebungsvariablen und überschreibe kwargs
        int_fields = ["mcp_port", "ollama_port", "ollama_timeout", "session_ttl", "rate_limit_requests_per_minute"]
        
        for env_key, config_key in env_mapping.items():
            env_value = os.getenv(env_key)
            if env_value is not None and config_key not in kwargs:
                if config_key in int_fields:
                    kwargs[config_key] = int(env_value)
                elif config_key == "session_storage_path":
                    kwargs[config_key] = Path(env_value)
                elif config_key == "rate_limit_enabled":
                    kwargs[config_key] = env_value.lower() in ("true", "1", "yes")
                else:
                    kwargs[config_key] = env_value

        super().__init__(**kwargs)


# Globale Konfigurationsinstanz
_config: Optional[Config] = None


def get_config() -> Config:
    """Gibt die globale Konfigurationsinstanz zurück."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(config: Config) -> None:
    """Setzt die globale Konfigurationsinstanz."""
    global _config
    _config = config

