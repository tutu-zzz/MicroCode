"""Context compiler orchestration."""

from __future__ import annotations

from collections.abc import Sequence

from microcode.context.models import ContextRequest, ContextSnapshot
from microcode.context.sources import ContextSource


class ContextCompiler:
    def __init__(self, sources: Sequence[ContextSource]) -> None:
        self.sources = tuple(sources)

    async def compile(self, request: ContextRequest) -> ContextSnapshot:
        del request
        raise NotImplementedError("Implement collect-score-select-render-snapshot in M5")
