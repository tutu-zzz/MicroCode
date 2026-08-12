"""Ensure the generated infrastructure document matches the current repository."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_infrastructure_document_is_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/update_infrastructure.py", "--check"],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
