"""Memory extraction boundary and deterministic test double."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from typing import Protocol

from pydantic import BaseModel, ConfigDict

from microcode.memory.models import MemoryCandidate


class MemoryExtractionRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    session_id: str
    turn_id: str
    evidence_event_ids: tuple[str, ...]


class MemoryExtractor(Protocol):
    async def extract(self, request: MemoryExtractionRequest) -> list[MemoryCandidate]: ...


class ScriptedMemoryExtractor:
    def __init__(self, batches: Iterable[list[MemoryCandidate]]) -> None:
        self._batches = deque(batches)
        self.requests: list[MemoryExtractionRequest] = []

    async def extract(self, request: MemoryExtractionRequest) -> list[MemoryCandidate]:
        self.requests.append(request)
        return self._batches.popleft() if self._batches else []
