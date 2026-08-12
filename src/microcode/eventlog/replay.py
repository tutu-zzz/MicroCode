"""Read-only state reconstruction and trace playback models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TraceItem(BaseModel):
    model_config = ConfigDict(frozen=True)
    stream_version: int
    event_id: str
    event_type: str
    summary: str
    turn_id: str | None = None
    causation_id: str | None = None
    correlation_id: str | None = None


class ReplayService:
    """Replay deliberately has no Provider or tool-executor dependency."""

    def timeline(self, stream_id: str) -> tuple[TraceItem, ...]:
        del stream_id
        raise NotImplementedError("Implement read-only timeline projection in M3")
