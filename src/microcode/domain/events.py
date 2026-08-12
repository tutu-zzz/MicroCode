"""Versioned event envelopes, payload schemas, and event construction."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from enum import StrEnum
from typing import cast
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from microcode.domain.json_types import JsonObject, JsonValue, validate_json_object


class EventType(StrEnum):
    SESSION_STARTED = "session.started"
    SESSION_RESUMED = "session.resumed"
    SESSION_PROVIDER_PINNED = "session.provider_pinned"
    TURN_STARTED = "turn.started"
    USER_MESSAGE_RECORDED = "user.message_recorded"
    CONTEXT_COMPILED = "context.compiled"
    MODEL_REQUESTED = "model.requested"
    MODEL_RESPONSE_COMPLETED = "model.response_completed"
    MODEL_FAILED = "model.failed"
    TOOL_REQUESTED = "tool.requested"
    TOOL_PREPARED = "tool.prepared"
    POLICY_DECIDED = "policy.decided"
    APPROVAL_REQUESTED = "approval.requested"
    APPROVAL_DECIDED = "approval.decided"
    TOOL_COMPLETED = "tool.completed"
    TOOL_FAILED = "tool.failed"
    ASSISTANT_MESSAGE_RECORDED = "assistant.message_recorded"
    TURN_COMPLETED = "turn.completed"
    TURN_FAILED = "turn.failed"
    MEMORY_CONSENT_RECORDED = "memory.consent_recorded"
    MEMORY_EXTRACTION_REQUESTED = "memory.extraction_requested"
    MEMORY_EXTRACTION_COMPLETED = "memory.extraction_completed"
    MEMORY_EXTRACTION_FAILED = "memory.extraction_failed"
    MEMORY_PROPOSED = "memory.proposed"
    MEMORY_ACCEPTED = "memory.accepted"
    MEMORY_REJECTED = "memory.rejected"
    MEMORY_SUPERSEDED = "memory.superseded"


class EventEnvelope(BaseModel):
    """Immutable event metadata plus a JSON-safe payload."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: int = 1
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    stream_id: str
    stream_version: int = Field(ge=1)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    event_type: str = Field(min_length=1)
    session_id: str | None = None
    run_id: str | None = None
    turn_id: str | None = None
    causation_id: str | None = None
    correlation_id: str | None = None
    payload: JsonObject

    @field_validator("occurred_at")
    @classmethod
    def require_utc_timestamp(cls, value: datetime) -> datetime:
        """Reject naive timestamps and normalize aware timestamps to UTC."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurred_at must include timezone information")
        return value.astimezone(UTC)

    @field_validator("payload", mode="before")
    @classmethod
    def require_json_payload(cls, value: object) -> JsonObject:
        return validate_json_object(value)


EventEnvelope.model_rebuild(_types_namespace={"JsonObject": JsonObject, "JsonValue": JsonValue})


class EventPayload(BaseModel):
    """Strict base model for event-specific payload schemas."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class SessionStarted(EventPayload):
    """Payload recorded when a new session stream is created."""

    project_root: str
    provider: str
    model: str


class UserMessageRecorded(EventPayload):
    """Payload linking a user message to durable text content."""

    text_ref: str


class UnknownEventTypeError(ValueError):
    """Raised when strict payload validation encounters an unknown event type."""


class DuplicatePayloadSchemaError(ValueError):
    """Raised when two payload schemas are registered for the same event type."""


class PayloadRegistry:
    """Map event names to payload models while preserving forward diagnostics."""

    def __init__(
        self,
        schemas: Mapping[EventType | str, type[EventPayload]] | None = None,
    ) -> None:
        self._schemas: dict[str, type[EventPayload]] = {}
        for event_type, schema in (schemas or {}).items():
            self.register(event_type, schema)

    def register(self, event_type: EventType | str, schema: type[EventPayload]) -> None:
        event_name = str(event_type)
        if event_name in self._schemas:
            raise DuplicatePayloadSchemaError(event_name)
        self._schemas[event_name] = schema

    def validate(
        self,
        event_type: EventType | str,
        payload: object,
        *,
        strict: bool = True,
    ) -> JsonObject:
        """Validate and normalize a payload for persistence.

        Unknown events fail in strict mode. Diagnostic readers may pass ``strict=False`` to retain
        an unknown but JSON-safe payload without projecting it.
        """

        event_name = str(event_type)
        schema = self._schemas.get(event_name)
        if schema is None:
            if strict:
                raise UnknownEventTypeError(event_name)
            return validate_json_object(payload)
        validated = schema.model_validate(payload)
        return validate_json_object(validated.model_dump(mode="json"))


DEFAULT_PAYLOAD_REGISTRY = PayloadRegistry(
    {
        EventType.SESSION_STARTED: SessionStarted,
        EventType.USER_MESSAGE_RECORDED: UserMessageRecorded,
    }
)


def create_event(
    *,
    stream_id: str,
    stream_version: int,
    event_type: EventType | str,
    payload: EventPayload | JsonObject,
    session_id: str | None = None,
    run_id: str | None = None,
    turn_id: str | None = None,
    causation_id: str | None = None,
    correlation_id: str | None = None,
    occurred_at: datetime | None = None,
    registry: PayloadRegistry = DEFAULT_PAYLOAD_REGISTRY,
) -> EventEnvelope:
    """Create a validated event without guessing its journal-owned stream version."""

    raw_payload: object
    if isinstance(payload, EventPayload):
        raw_payload = payload.model_dump(mode="python")
    else:
        raw_payload = payload
    fields: dict[str, object] = {
        "stream_id": stream_id,
        "stream_version": stream_version,
        "event_type": str(event_type),
        "payload": registry.validate(event_type, raw_payload),
        "session_id": session_id,
        "run_id": run_id,
        "turn_id": turn_id,
        "causation_id": causation_id,
        "correlation_id": correlation_id,
    }
    if occurred_at is not None:
        fields["occurred_at"] = occurred_at
    return EventEnvelope.model_validate(cast(object, fields))
