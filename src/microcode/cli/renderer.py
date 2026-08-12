"""Rich-based rendering adapter boundary."""

from __future__ import annotations

from microcode.eventlog.replay import TraceItem


class Renderer:
    def print_banner(self) -> None:
        print("MicroCode — observable agent core")

    def print_text_delta(self, text: str) -> None:
        print(text, end="", flush=True)

    def print_trace(self, items: tuple[TraceItem, ...]) -> None:
        for item in items:
            print(f"{item.stream_version:04d} {item.event_type} {item.summary}")
