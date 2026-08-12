"""Context source contracts and built-in source boundaries."""

from __future__ import annotations

from typing import Protocol

from microcode.context.models import ContextCandidate, ContextRequest


class ContextSource(Protocol):
    name: str

    async def collect(self, request: ContextRequest) -> list[ContextCandidate]: ...


class ProjectInstructionSource:
    """Collect root-to-cwd AGENTS.md and MICRO.md files in M5."""

    name = "project_instructions"

    async def collect(self, request: ContextRequest) -> list[ContextCandidate]:
        del request
        raise NotImplementedError("Implement deterministic instruction discovery in M5")


class MemorySource:
    """Expose active memory claims as candidates after M11."""

    name = "memory"

    async def collect(self, request: ContextRequest) -> list[ContextCandidate]:
        del request
        return []
