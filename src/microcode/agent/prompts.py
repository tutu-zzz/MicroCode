"""Small, explicit system instruction builders."""

from pathlib import Path


def base_system_prompt(project_root: Path) -> str:
    return (
        "You are MicroCode, a coding agent working inside "
        f"{project_root}. Inspect before editing, use structured tools, "
        "and respect policy decisions."
    )
