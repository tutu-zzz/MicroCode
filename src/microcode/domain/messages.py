"""Portable message and content block models."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from microcode.domain.json_types import JsonObject


class ContentRef(BaseModel):
    """Either inline content or a content-addressed artifact reference."""

    model_config = ConfigDict(frozen=True)

    inline_text: str | None = None
    artifact_digest: str | None = None
    preview: str | None = None
    digest: str
    size: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_storage(self) -> ContentRef:
        if (self.inline_text is None) == (self.artifact_digest is None):
            raise ValueError("exactly one of inline_text or artifact_digest is required")
        return self


class TextBlock(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal["text"] = "text"
    text: str


class ToolUseBlock(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal["tool_use"] = "tool_use"
    tool_call_id: str
    name: str
    arguments: JsonObject


class ToolResultBlock(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal["tool_result"] = "tool_result"
    tool_call_id: str
    content: ContentRef
    is_error: bool = False


ContentBlock = Annotated[TextBlock | ToolUseBlock | ToolResultBlock, Field(discriminator="type")]


class ModelMessage(BaseModel):
    model_config = ConfigDict(frozen=True)
    role: Literal["user", "assistant"]
    blocks: tuple[ContentBlock, ...]
