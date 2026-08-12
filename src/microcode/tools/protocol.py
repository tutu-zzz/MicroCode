"""Uniform tool prepare/execute protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from microcode.actions.models import PreparedAction
from microcode.domain.json_types import JsonObject
from microcode.domain.messages import ContentRef
from microcode.provider.protocol import ToolDefinition


class ToolContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    project_root: Path
    cwd: Path
    session_id: str


class PreparedToolCall(BaseModel):
    model_config = ConfigDict(frozen=True)
    tool_call_id: str
    tool_name: str
    normalized_input: JsonObject
    action: PreparedAction | None = None


class ToolResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    content: ContentRef
    summary: str
    is_error: bool = False
    metadata: JsonObject = Field(default_factory=dict)


class Tool(Protocol):
    name: str
    description: str
    input_model: type[BaseModel]

    def definition(self) -> ToolDefinition: ...
    async def prepare(self, raw_input: JsonObject, context: ToolContext) -> PreparedToolCall: ...
    async def execute(self, prepared: PreparedToolCall, context: ToolContext) -> ToolResult: ...


def definition_for(tool: Tool) -> ToolDefinition:
    """Generate provider JSON Schema from the same Pydantic model used for validation."""

    return ToolDefinition(
        name=tool.name,
        description=tool.description,
        input_schema=tool.input_model.model_json_schema(),
    )
