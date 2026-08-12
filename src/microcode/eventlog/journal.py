"""Event journal contracts and JSONL implementation boundary."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from microcode.domain.events import EventEnvelope, EventType
from microcode.domain.json_types import JsonObject


class ConcurrencyError(RuntimeError):
    """Raised when expected and actual stream versions differ."""


class CorruptEventLogError(RuntimeError):
    """Raised when a stream cannot be parsed safely."""


class EventJournal(Protocol):
    def append(
        self,
        *,
        stream_id: str,
        expected_version: int,
        event_type: EventType,
        payload: JsonObject,
        session_id: str | None = None,
        run_id: str | None = None,
        turn_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> EventEnvelope: ...

    def read(self, stream_id: str, after_version: int = 0) -> Iterable[EventEnvelope]: ...


class JsonlEventJournal:
    """File-backed journal implemented in M2."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def append(self, **_: object) -> EventEnvelope:
        raise NotImplementedError("Implement locked append with expected-version checks in M2")

    def read(self, stream_id: str, after_version: int = 0) -> Iterable[EventEnvelope]:
        del stream_id, after_version
        raise NotImplementedError("Implement strict JSONL reading in M2")
