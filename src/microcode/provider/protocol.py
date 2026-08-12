"""Provider-neutral model request and streaming response protocol."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Literal, Protocol, TypeAlias

from pydantic import BaseModel, ConfigDict

from microcode.domain.json_types import JsonObject
from microcode.domain.messages import ContentBlock, ModelMessage, TextBlock


class ToolDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    description: str
    input_schema: JsonObject


class ModelRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    provider: str
    model: str
    system_blocks: tuple[TextBlock, ...]
    messages: tuple[ModelMessage, ...]
    tools: tuple[ToolDefinition, ...]
    max_output_tokens: int


class Usage(BaseModel):
    model_config = ConfigDict(frozen=True)
    input_tokens: int | None = None
    output_tokens: int | None = None


class TextDelta(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal["text_delta"] = "text_delta"
    text: str


class ResponseCompleted(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal["response_completed"] = "response_completed"
    blocks: tuple[ContentBlock, ...]
    usage: Usage | None = None
    stop_reason: str | None = None
    native_artifact_digest: str | None = None


ProviderEvent: TypeAlias = TextDelta | ResponseCompleted


class Provider(Protocol):
    name: str

    def stream(self, request: ModelRequest) -> AsyncIterator[ProviderEvent]: ...
