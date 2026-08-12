"""Validated application paths and configuration models."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class AppPaths(BaseModel):
    """Filesystem locations for generated local state."""

    model_config = ConfigDict(frozen=True)

    home: Path

    @property
    def events(self) -> Path:
        return self.home / "events"

    @property
    def artifacts(self) -> Path:
        return self.home / "artifacts" / "sha256"

    @property
    def snapshots(self) -> Path:
        return self.home / "snapshots"

    @property
    def locks(self) -> Path:
        return self.home / "locks"


class AgentLimits(BaseModel):
    """Hard limits that prevent unbounded agent turns."""

    model_config = ConfigDict(frozen=True)

    max_model_iterations: int = Field(default=20, ge=1)
    max_tool_calls: int = Field(default=10, ge=0)
    max_turn_seconds: int = Field(default=600, ge=1)


def default_app_paths() -> AppPaths:
    configured = os.environ.get("MICROCODE_HOME")
    return AppPaths(
        home=Path(configured).expanduser() if configured else Path.home() / ".microcode"
    )
