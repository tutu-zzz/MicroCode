"""list_files, read_file, edit_file, and write_file tool boundaries."""

from __future__ import annotations

from pydantic import BaseModel, Field

from microcode.domain.json_types import JsonObject
from microcode.provider.protocol import ToolDefinition
from microcode.tools.protocol import PreparedToolCall, ToolContext, ToolResult, definition_for


class ListFilesInput(BaseModel):
    path: str = "."
    pattern: str | None = None
    max_results: int = Field(default=200, ge=1, le=2_000)


class ReadFileInput(BaseModel):
    path: str
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=200, ge=1, le=2_000)


class EditFileInput(BaseModel):
    path: str
    old_text: str
    new_text: str


class WriteFileInput(BaseModel):
    path: str
    content: str


class _FilesystemTool:
    name: str
    description = ""
    input_model: type[BaseModel]

    def definition(self) -> ToolDefinition:
        return definition_for(self)

    async def prepare(self, raw_input: JsonObject, context: ToolContext) -> PreparedToolCall:
        del raw_input, context
        raise NotImplementedError("Implement safe path normalization and preparation in M7-M8")

    async def execute(self, prepared: PreparedToolCall, context: ToolContext) -> ToolResult:
        del prepared, context
        raise NotImplementedError("Implement filesystem execution in M7-M8")


class ListFilesTool(_FilesystemTool):
    name = "list_files"
    description = "List files inside the current project with stable ordering."
    input_model = ListFilesInput


class ReadFileTool(_FilesystemTool):
    name = "read_file"
    description = "Read a range of lines from a UTF-8 text file in the project."
    input_model = ReadFileInput


class EditFileTool(_FilesystemTool):
    name = "edit_file"
    description = "Prepare an exact single replacement and show a diff before writing."
    input_model = EditFileInput


class WriteFileTool(_FilesystemTool):
    name = "write_file"
    description = "Prepare creation or replacement of one text file with diff review."
    input_model = WriteFileInput
