"""Immutable context compiler inputs and outputs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from microcode.domain.json_types import JsonObject
from microcode.domain.messages import ContentRef


class ContextBudget(BaseModel):
    model_config = ConfigDict(frozen=True)
    model_limit: int = Field(default=128_000, ge=1)
    reserved_output: int = Field(default=8_000, ge=0)
    reserved_tools: int = Field(default=12_000, ge=0)
    safety_margin: int = Field(default=8_000, ge=0)

    @property
    def available_input(self) -> int:
        return self.model_limit - self.reserved_output - self.reserved_tools - self.safety_margin


class ContextCandidate(BaseModel):
    model_config = ConfigDict(frozen=True)
    candidate_id: str
    source: str
    scope: str
    label: str
    content: ContentRef
    content_digest: str
    estimated_tokens: int = Field(ge=0)
    metadata: JsonObject = Field(default_factory=dict)


class ScoredCandidate(BaseModel):
    model_config = ConfigDict(frozen=True)
    candidate: ContextCandidate
    score: float
    factors: dict[str, float] = Field(default_factory=dict)


class ContextDecision(BaseModel):
    model_config = ConfigDict(frozen=True)
    candidate_id: str
    included: bool
    reason: str
    final_position: int | None = None


class ContextSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True)
    snapshot_id: str
    budget: ContextBudget
    candidates: tuple[ScoredCandidate, ...]
    decisions: tuple[ContextDecision, ...]
    rendered_context: ContentRef
    rendered_digest: str


class ContextRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    session_id: str
    project_root: str
    cwd: str
    user_text: str
