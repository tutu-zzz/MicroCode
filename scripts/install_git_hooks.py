"""Configure this repository to use the committed .githooks directory."""

from __future__ import annotations

import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Git repository not found. Initialize Git before installing hooks.")
        return 1

    repository_root = Path(result.stdout.strip()).resolve()
    if repository_root != PROJECT_ROOT:
        print(f"Expected Git root {PROJECT_ROOT}, found {repository_root}.")
        return 1

    subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=PROJECT_ROOT,
        check=True,
    )
    print("Git hooks enabled from .githooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

