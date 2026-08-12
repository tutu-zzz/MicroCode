"""Session lifecycle application service."""

from __future__ import annotations

from pathlib import Path

from microcode.eventlog.journal import EventJournal
from microcode.session.models import SessionState, SessionSummary


class SessionService:
    def __init__(self, journal: EventJournal) -> None:
        self.journal = journal

    def create(self, project_root: Path, provider: str, model: str) -> SessionState:
        del project_root, provider, model
        raise NotImplementedError("Implement event-sourced session creation in M3")

    def load(self, session_id: str) -> SessionState:
        del session_id
        raise NotImplementedError("Implement projection loading in M3")

    def list_for_project(self, project_root: Path) -> tuple[SessionSummary, ...]:
        del project_root
        raise NotImplementedError("Implement the rebuildable session index in M3")
