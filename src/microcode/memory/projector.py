"""Pure projection of active, rejected, and superseded memory claims."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from microcode.domain.events import EventEnvelope
from microcode.memory.models import MemoryClaim


class MemoryState(BaseModel):
    model_config = ConfigDict(frozen=True)
    claims: dict[str, MemoryClaim] = Field(default_factory=dict)
    stream_version: int = 0


def apply_memory_event(state: MemoryState, event: EventEnvelope) -> MemoryState:
    del event
    raise NotImplementedError("Implement immutable memory projection in M11")
