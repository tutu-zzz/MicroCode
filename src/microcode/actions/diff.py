"""Unified diff generation using the Python standard library."""

from __future__ import annotations

from difflib import unified_diff


def make_unified_diff(path: str, before: str, after: str) -> str:
    return "".join(
        unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
        )
    )
