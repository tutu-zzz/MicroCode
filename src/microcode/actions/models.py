"""Serializable actions prepared before policy and approval."""

from __future__ import annotations

from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from microcode.domain.json_types import JsonObject
from microcode.domain.messages import ContentRef


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PreparedAction(BaseModel):
    model_config = ConfigDict(frozen=True)
    action_id: str = Field(default_factory=lambda: str(uuid4()))
    tool_call_id: str
    effect: str
    normalized_target: str | None = None
    preview: ContentRef | None = None
    before_digest: str | None = None
    risk: RiskLevel
    executable: JsonObject
