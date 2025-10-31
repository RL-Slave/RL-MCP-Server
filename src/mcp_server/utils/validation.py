"""Parameter-Validierung für Tools."""

from typing import Any, Dict, Type, get_type_hints

from pydantic import BaseModel, ValidationError as PydanticValidationError

from mcp_server.exceptions import ValidationError


def validate_params(params: Dict[str, Any], schema: Type[BaseModel]) -> BaseModel:
    """Validiert Parameter gegen ein Pydantic-Schema."""
    try:
        return schema(**params)
    except PydanticValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        raise ValidationError(f"Validierungsfehler: {'; '.join(errors)}")


def validate_model_name(model: str) -> str:
    """Validiert einen Modellnamen."""
    if not model or not isinstance(model, str):
        raise ValidationError("Modellname muss ein nicht-leerer String sein")
    if len(model.strip()) == 0:
        raise ValidationError("Modellname darf nicht leer sein")
    return model.strip()

