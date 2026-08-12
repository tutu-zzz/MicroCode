"""Application composition root.

The runtime will wire concrete adapters to domain protocols without moving business state into
the CLI. It is intentionally minimal until the event kernel is implemented in M1-M3.
"""

from __future__ import annotations

from dataclasses import dataclass

from microcode.config import AppPaths


@dataclass(frozen=True, slots=True)
class RuntimeSettings:
    paths: AppPaths
    project_root: str
    provider: str
    model: str


class MicroCodeRuntime:
    """Top-level application service assembled incrementally by the tutorial."""

    def __init__(self, settings: RuntimeSettings) -> None:
        self.settings = settings

    async def run(self) -> None:
        raise NotImplementedError("Implement the runtime composition after M1-M10")
