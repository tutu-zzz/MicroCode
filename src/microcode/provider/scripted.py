"""Deterministic provider used by unit tests and golden traces."""

from __future__ import annotations

from collections import deque
from collections.abc import AsyncIterator, Iterable

from microcode.provider.protocol import ModelRequest, ProviderEvent, ResponseCompleted, TextDelta


class ScriptExhaustedError(RuntimeError):
    """Raised when a scripted scenario asks for more responses than supplied."""


class ScriptedProvider:
    name = "scripted"

    def __init__(self, responses: Iterable[ResponseCompleted]) -> None:
        self._responses = deque(responses)
        self.requests: list[ModelRequest] = []

    async def stream(self, request: ModelRequest) -> AsyncIterator[ProviderEvent]:
        self.requests.append(request)
        if not self._responses:
            raise ScriptExhaustedError("scripted provider response queue is empty")
        response = self._responses.popleft()
        for block in response.blocks:
            if block.type == "text":
                yield TextDelta(text=block.text)
        yield response
