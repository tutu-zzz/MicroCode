"""Console entry point for MicroCode."""

from __future__ import annotations

import argparse
import asyncio
from collections.abc import Sequence

from microcode import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="microcode",
        description="An observable, explainable, and replayable coding agent.",
    )
    parser.add_argument(
        "path", nargs="?", default=".", help="Project path (default: current directory)"
    )
    parser.add_argument("--resume", metavar="SESSION_ID", help="Resume an existing session")
    parser.add_argument(
        "--replay", metavar="SESSION_ID", help="Replay a session without side effects"
    )
    parser.add_argument("--step", action="store_true", help="Pause after each replay event")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


async def async_main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    mode = "replay" if args.replay else "resume" if args.resume else "new session"
    print(f"MicroCode {__version__} architecture scaffold ({mode})")
    print("Follow doc/plan.md from M0 to implement the MVP.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    return asyncio.run(async_main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
