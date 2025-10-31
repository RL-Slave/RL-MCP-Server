"""Custom Exceptions für den MCP Server."""


class MCPError(Exception):
    """Basis-Exception für MCP Server Fehler."""

    pass


class OllamaConnectionError(MCPError):
    """Fehler bei der Verbindung zu Ollama."""

    pass


class OllamaAPIError(MCPError):
    """Fehler bei Ollama API Anfragen."""

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class ToolError(MCPError):
    """Fehler bei Tool-Ausführung."""

    pass


class ValidationError(MCPError):
    """Fehler bei Parameter-Validierung."""

    pass


class ConfigError(MCPError):
    """Fehler bei Konfiguration."""

    pass

