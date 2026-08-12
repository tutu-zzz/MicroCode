"""Bounded agent turn orchestration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TurnResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    turn_id: str
    final_text: str
    model_iterations: int
    tool_calls: int


class AgentLoop:
    """Implemented with ScriptedProvider before the real provider is connected."""

    async def run_turn(self, user_text: str) -> TurnResult:
        del user_text
        raise NotImplementedError("Implement the event-recorded bounded loop in M6")
