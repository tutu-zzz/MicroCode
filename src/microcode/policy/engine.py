"""Deterministic deny/allow/ask rule evaluation."""

from __future__ import annotations

from pathlib import Path

from microcode.actions.models import PreparedAction
from microcode.policy.models import PolicyDecision


class PolicyEngine:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()

    def decide(self, action: PreparedAction) -> PolicyDecision:
        del action
        raise NotImplementedError("Implement balanced path and command rules in M8")
