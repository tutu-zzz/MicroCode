"""Session projection models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from microcode.domain.messages import ModelMessage


class SessionState(BaseModel):
    """A rebuildable view; never the source of truth."""

    model_config = ConfigDict(frozen=True)

    session_id: str
    project_root: str
    provider: str
    model: str
    stream_version: int = 0
    status: str = "active"
    messages: tuple[ModelMessage, ...] = ()
    latest_context_snapshot_id: str | None = None
    active_turn_id: str | None = None


class SessionSummary(BaseModel):
    model_config = ConfigDict(frozen=True)
    session_id: str
    project_root: str
    provider: str
    model: str
    stream_version: int
    status: str
