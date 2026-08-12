"""Pure session event projection."""

from __future__ import annotations

from microcode.domain.events import EventEnvelope, EventType
from microcode.session.models import SessionState


def apply_session_event(
    state: SessionState | None,
    event: EventEnvelope,
) -> SessionState:
    """Fold one event into state without I/O, time, randomness, or external calls."""

    if event.event_type == EventType.SESSION_STARTED:
        if state is not None:
            raise ValueError("session.started must be the first event")
        payload = event.payload
        return SessionState(
            session_id=str(payload["session_id"]),
            project_root=str(payload["project_root"]),
            provider=str(payload["provider"]),
            model=str(payload["model"]),
            stream_version=event.stream_version,
        )

    if state is None:
        raise ValueError(f"{event.event_type} cannot precede session.started")

    updates: dict[str, object] = {"stream_version": event.stream_version}
    if event.event_type == EventType.TURN_STARTED:
        updates["active_turn_id"] = event.turn_id
    elif event.event_type in {EventType.TURN_COMPLETED, EventType.TURN_FAILED}:
        updates["active_turn_id"] = None
    elif event.event_type == EventType.CONTEXT_COMPILED:
        updates["latest_context_snapshot_id"] = str(event.payload["snapshot_id"])
    return state.model_copy(update=updates)


def rebuild_session(events: list[EventEnvelope]) -> SessionState:
    state: SessionState | None = None
    for event in events:
        state = apply_session_event(state, event)
    if state is None:
        raise ValueError("cannot rebuild a session from an empty event stream")
    return state
