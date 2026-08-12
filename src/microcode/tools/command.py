"""Structured executable-plus-arguments command tool."""

from __future__ import annotations

from pydantic import BaseModel, Field

from microcode.domain.json_types import JsonObject
from microcode.provider.protocol import ToolDefinition
from microcode.tools.protocol import PreparedToolCall, ToolContext, ToolResult, definition_for


class RunCommandInput(BaseModel):
    executable: str
    args: list[str] = Field(default_factory=list)
    timeout_seconds: int = Field(default=60, ge=1, le=600)


class RunCommandTool:
    name = "run_command"
    description = "Run one executable with structured arguments and no implicit shell."
    input_model: type[BaseModel] = RunCommandInput

    def definition(self) -> ToolDefinition:
        return definition_for(self)

    async def prepare(self, raw_input: JsonObject, context: ToolContext) -> PreparedToolCall:
        del raw_input, context
        raise NotImplementedError("Implement command preparation and policy subject in M8")

    async def execute(self, prepared: PreparedToolCall, context: ToolContext) -> ToolResult:
        del prepared, context
        raise NotImplementedError("Implement create_subprocess_exec execution in M8")
