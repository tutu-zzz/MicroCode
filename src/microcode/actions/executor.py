"""Side-effect executor boundary."""

from __future__ import annotations

from typing import Protocol

from microcode.actions.models import PreparedAction
from microcode.tools.protocol import ToolResult


class StalePreparedActionError(RuntimeError):
    """Raised when the target changed after approval."""


class ActionExecutor(Protocol):
    async def execute(self, action: PreparedAction) -> ToolResult: ...


class LocalActionExecutor:
    async def execute(self, action: PreparedAction) -> ToolResult:
        del action
        raise NotImplementedError("Implement digest checks and atomic effects in M8")
