"""Consent-aware synchronous memory workflow."""

from __future__ import annotations

from microcode.memory.extractor import MemoryExtractor


class MemoryService:
    def __init__(self, extractor: MemoryExtractor) -> None:
        self.extractor = extractor

    async def process_completed_turn(self, session_id: str, turn_id: str) -> None:
        del session_id, turn_id
        raise NotImplementedError("Implement consent, evidence validation, and supersession in M11")
