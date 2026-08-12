"""Anthropic Messages compatible provider adapter."""

from __future__ import annotations

from collections.abc import AsyncIterator

from microcode.provider.protocol import ModelRequest, ProviderEvent


class AnthropicProvider:
    """Implemented and contract-tested in M9.

    The concrete SDK remains isolated here so the agent loop never depends on Anthropic types.
    """

    name = "anthropic"

    def __init__(self, *, api_key: str, model: str, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    async def stream(self, request: ModelRequest) -> AsyncIterator[ProviderEvent]:
        del request
        raise NotImplementedError("Implement Anthropic/Kimi-compatible streaming in M9")
        yield  # pragma: no cover
