"""Response-Formatierung für Tools."""

from typing import Any, Dict


def format_model_list(response: Dict[str, Any]) -> Dict[str, Any]:
    """Formatiert die Modell-Liste."""
    models = response.get("models", [])
    return {
        "models": [
            {
                "name": model.get("name", ""),
                "size": model.get("size", 0),
                "modified_at": model.get("modified_at", ""),
                "digest": model.get("digest", ""),
            }
            for model in models
        ],
        "count": len(models),
    }


def format_generate_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Formatiert eine Generate-Response."""
    return {
        "response": response.get("response", ""),
        "done": response.get("done", False),
        "context": response.get("context", []),
        "total_duration": response.get("total_duration", 0),
        "load_duration": response.get("load_duration", 0),
        "prompt_eval_count": response.get("prompt_eval_count", 0),
        "prompt_eval_duration": response.get("prompt_eval_duration", 0),
        "eval_count": response.get("eval_count", 0),
        "eval_duration": response.get("eval_duration", 0),
    }


def format_chat_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Formatiert eine Chat-Response."""
    return {
        "message": response.get("message", {}),
        "done": response.get("done", False),
        "total_duration": response.get("total_duration", 0),
        "load_duration": response.get("load_duration", 0),
        "prompt_eval_count": response.get("prompt_eval_count", 0),
        "prompt_eval_duration": response.get("prompt_eval_duration", 0),
        "eval_count": response.get("eval_count", 0),
        "eval_duration": response.get("eval_duration", 0),
    }


def format_embedding_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Formatiert eine Embedding-Response."""
    return {
        "embedding": response.get("embedding", []),
    }


def format_error(error: Exception) -> Dict[str, Any]:
    """Formatiert einen Fehler."""
    return {
        "error": str(error),
        "error_type": type(error).__name__,
    }

