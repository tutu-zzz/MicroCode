"""Prompt-toolkit REPL and application command routing."""

from __future__ import annotations


class CliApp:
    async def run(self) -> None:
        raise NotImplementedError("Implement the async REPL, commands, and approvals in M10")
