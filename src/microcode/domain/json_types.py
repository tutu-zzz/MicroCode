"""Recursive JSON types and strict validation for durable schemas."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import TypeAlias

from typing_extensions import TypeAliasType

JsonScalar: TypeAlias = str | int | float | bool | None
# Pydantic requires a named recursive alias on Python 3.11/3.12. Mypy 2.3 cannot resolve the
# quoted self-reference inside TypeAliasType, so this definition has a narrowly scoped exception.
JsonValue = TypeAliasType(  # type: ignore[misc]
    "JsonValue",
    JsonScalar | list["JsonValue"] | dict[str, "JsonValue"],  # type: ignore[misc]
)
JsonObject: TypeAlias = dict[str, JsonValue]  # type: ignore[misc]


class JsonValueError(ValueError):
    """Raised when a durable value cannot be represented by JSON without coercion."""


def validate_json_value(value: object, *, path: str = "$") -> JsonValue:
    """Return a JSON-safe copy of *value*, rejecting Python-specific objects.

    Validation is intentionally strict: tuples are not silently converted to arrays, mapping
    keys must already be strings, and non-finite floats are rejected because JSON cannot represent
    them portably.
    """

    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise JsonValueError(f"{path} contains a non-finite float")
        return value
    if isinstance(value, list):
        return [
            validate_json_value(item, path=f"{path}[{index}]") for index, item in enumerate(value)
        ]
    if isinstance(value, Mapping):
        result: JsonObject = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise JsonValueError(f"{path} contains a non-string object key")
            result[key] = validate_json_value(item, path=f"{path}.{key}")
        return result
    raise JsonValueError(f"{path} contains unsupported value type {type(value).__name__}")


def validate_json_object(value: object) -> JsonObject:
    """Return a JSON-safe object copy without applying lossy type coercion."""

    validated = validate_json_value(value)
    if not isinstance(validated, dict):
        raise JsonValueError("$ must be a JSON object")
    return validated
