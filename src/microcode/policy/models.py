"""Permission decisions and approval port."""

from __future__ import annotations

from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel, ConfigDict

from microcode.actions.models import PreparedAction, RiskLevel


class DecisionKind(StrEnum):
    ALLOW = "allow"
    ASK = "ask"
    DENY = "deny"


class PolicyDecision(BaseModel):
    model_config = ConfigDict(frozen=True)
    decision: DecisionKind
    rule_id: str
    reason: str
    risk: RiskLevel


class ApprovalPort(Protocol):
    async def request(self, action: PreparedAction, decision: PolicyDecision) -> bool: ...
