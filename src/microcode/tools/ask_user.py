"""Model-initiated user question tool, separate from safety approval."""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, Field

from microcode.domain.json_types import JsonObject
from microcode.provider.protocol import ToolDefinition
from microcode.tools.protocol import PreparedToolCall, ToolContext, ToolResult, definition_for


class AskUserInput(BaseModel):
    question: str = Field(min_length=1, max_length=1_000)
    choices: list[str] = Field(default_factory=list, max_length=10)


class UserInputPort(Protocol):
    async def ask(self, question: str, choices: tuple[str, ...]) -> str: ...


class AskUserTool:
    name = "ask_user"
    description = "Ask the user one blocking product or implementation question."
    input_model: type[BaseModel] = AskUserInput

    def __init__(self, user_input: UserInputPort) -> None:
        self.user_input = user_input

    def definition(self) -> ToolDefinition:
        return definition_for(self)

    async def prepare(self, raw_input: JsonObject, context: ToolContext) -> PreparedToolCall:
        del raw_input, context
        raise NotImplementedError("Implement validated question preparation in M8")

    async def execute(self, prepared: PreparedToolCall, context: ToolContext) -> ToolResult:
        del prepared, context
        raise NotImplementedError("Implement UserInputPort execution in M8")
