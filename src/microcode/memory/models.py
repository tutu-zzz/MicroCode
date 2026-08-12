"""Traceable memory claims and extraction candidates."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class MemoryClaim(BaseModel):
    model_config = ConfigDict(frozen=True)
    memory_id: str = Field(default_factory=lambda: str(uuid4()))
    scope: Literal["user", "project", "session"]
    kind: str
    key: str
    claim: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_event_ids: tuple[str, ...]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: Literal["active", "rejected", "superseded"] = "active"
    supersedes: str | None = None


class MemoryCandidate(BaseModel):
    model_config = ConfigDict(frozen=True)
    scope: Literal["user", "project", "session"]
    kind: str
    key: str
    claim: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_event_ids: tuple[str, ...]
    supersedes: str | None = None
