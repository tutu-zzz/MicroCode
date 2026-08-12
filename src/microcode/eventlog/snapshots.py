"""Rebuildable projection snapshot boundary."""

from __future__ import annotations

from pathlib import Path
from typing import Generic, TypeVar

T = TypeVar("T")


class SnapshotStore(Generic[T]):
    def __init__(self, root: Path) -> None:
        self.root = root

    def load(self, stream_id: str) -> tuple[int, T] | None:
        del stream_id
        raise NotImplementedError("Implement rebuildable snapshots in M3")

    def save(self, stream_id: str, stream_version: int, state: T) -> None:
        del stream_id, stream_version, state
        raise NotImplementedError("Implement atomic snapshot writes in M3")
