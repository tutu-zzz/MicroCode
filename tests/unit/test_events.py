"""Contract tests for durable event envelopes and payload schemas."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from microcode.domain.events import (
    DEFAULT_PAYLOAD_REGISTRY,
    EventEnvelope,
    EventType,
    SessionStarted,
    UnknownEventTypeError,
    create_event,
)


def session_started_event(**overrides: object) -> EventEnvelope:
    fields: dict[str, object] = {
        "stream_id": "session:test-session",
        "stream_version": 1,
        "event_type": EventType.SESSION_STARTED,
        "session_id": "test-session",
        "payload": {
            "project_root": "D:/project",
            "provider": "scripted",
            "model": "test-model",
        },
    }
    fields.update(overrides)
    return EventEnvelope.model_validate(fields)


def test_event_round_trips_as_one_line_json() -> None:
    event = session_started_event()

    line = event.model_dump_json()
    restored = EventEnvelope.model_validate_json(line)

    assert "\n" not in line
    assert restored == event
    assert restored.occurred_at.tzinfo is UTC


def test_event_factory_validates_a_known_payload() -> None:
    event = create_event(
        stream_id="session:test-session",
        stream_version=1,
        event_type=EventType.SESSION_STARTED,
        session_id="test-session",
        payload=SessionStarted(
            project_root="D:/project",
            provider="scripted",
            model="test-model",
        ),
    )

    assert event.event_type == "session.started"
    assert event.payload["provider"] == "scripted"


def test_naive_timestamp_is_rejected() -> None:
    with pytest.raises(ValidationError, match="timezone information"):
        session_started_event(occurred_at=datetime(2026, 8, 12, 12, 0, 0))


def test_aware_timestamp_is_normalized_to_utc() -> None:
    event = session_started_event(
        occurred_at=datetime(2026, 8, 12, 12, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    )

    assert event.occurred_at == datetime(2026, 8, 12, 4, 0, 0, tzinfo=UTC)
    assert event.occurred_at.tzinfo is UTC


def test_extra_envelope_field_is_rejected() -> None:
    with pytest.raises(ValidationError, match="unexpected_field"):
        session_started_event(unexpected_field=True)


@pytest.mark.parametrize("invalid", [Path("private.txt"), object()])
def test_python_objects_cannot_enter_payload(invalid: object) -> None:
    with pytest.raises(ValidationError, match="unsupported value type"):
        session_started_event(payload={"value": invalid})


def test_event_is_frozen() -> None:
    event = session_started_event()

    with pytest.raises(ValidationError, match="frozen"):
        event.stream_version = 2


def test_registry_rejects_misspelled_known_payload_field() -> None:
    with pytest.raises(ValidationError, match="project_rooot"):
        DEFAULT_PAYLOAD_REGISTRY.validate(
            EventType.SESSION_STARTED,
            {
                "project_root": "D:/project",
                "project_rooot": "D:/wrong",
                "provider": "scripted",
                "model": "test-model",
            },
        )


def test_registry_can_retain_unknown_json_payload_for_diagnostics() -> None:
    payload = {"future": [1, "two", True]}

    with pytest.raises(UnknownEventTypeError, match="future.event"):
        DEFAULT_PAYLOAD_REGISTRY.validate("future.event", payload)

    assert DEFAULT_PAYLOAD_REGISTRY.validate("future.event", payload, strict=False) == payload
