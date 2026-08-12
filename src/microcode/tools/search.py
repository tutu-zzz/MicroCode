"""Structured ripgrep-backed search tool."""

from __future__ import annotations

from pydantic import BaseModel, Field

from microcode.domain.json_types import JsonObject
from microcode.provider.protocol import ToolDefinition
from microcode.tools.protocol import PreparedToolCall, ToolContext, ToolResult, definition_for


class SearchTextInput(BaseModel):
    pattern: str
    path: str = "."
    glob: str | None = None
    max_results: int = Field(default=200, ge=1, le=2_000)


class SearchTextTool:
    name = "search_text"
    description = "Search project text with ripgrep and return bounded structured matches."
    input_model: type[BaseModel] = SearchTextInput

    def definition(self) -> ToolDefinition:
        return definition_for(self)

    async def prepare(self, raw_input: JsonObject, context: ToolContext) -> PreparedToolCall:
        del raw_input, context
        raise NotImplementedError("Implement rg argument preparation in M7")

    async def execute(self, prepared: PreparedToolCall, context: ToolContext) -> ToolResult:
        del prepared, context
        raise NotImplementedError("Implement shell-free rg execution in M7")
