"""Slash-command parsing independent from the interactive REPL."""

from __future__ import annotations

import shlex
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SlashCommand:
    name: str
    args: tuple[str, ...] = ()


def parse_slash_command(text: str) -> SlashCommand | None:
    stripped = text.strip()
    if not stripped.startswith("/"):
        return None
    parts = shlex.split(stripped[1:])
    if not parts:
        raise ValueError("slash command name is required")
    return SlashCommand(name=parts[0].casefold(), args=tuple(parts[1:]))
