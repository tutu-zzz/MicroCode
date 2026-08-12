"""Stable tool registration and lookup."""

from __future__ import annotations

from microcode.provider.protocol import ToolDefinition
from microcode.tools.protocol import Tool, definition_for


class DuplicateToolError(ValueError):
    pass


class ToolNotFoundError(KeyError):
    pass


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise DuplicateToolError(tool.name)
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as error:
            raise ToolNotFoundError(name) from error

    def definitions(self) -> tuple[ToolDefinition, ...]:
        return tuple(definition_for(self._tools[name]) for name in sorted(self._tools))
