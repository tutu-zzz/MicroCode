# MicroCode

MicroCode is an observable, explainable, and replayable command-line coding agent.

The repository is currently at the architecture-scaffold stage. The implementation is built
incrementally by following [`doc/plan.md`](doc/plan.md). Product requirements and MVP boundaries
are defined in [`doc/prd.md`](doc/prd.md).

## Development setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
microcode --help
```

## Quality checks

```powershell
pytest -m "not integration"
ruff check src tests
ruff format --check src tests
mypy src
```

Generated sessions, events, artifacts, and memories will live under `~/.microcode`, not inside
the project being operated on.

Chinese documentation: [`README.zh-CN.md`](README.zh-CN.md)

## Architecture document

[`doc/infrastructure.md`](doc/infrastructure.md) is generated from the repository tree and module
docstrings. After a development change, run:

```powershell
python scripts/update_infrastructure.py
python scripts/update_infrastructure.py --check
```

Run `python scripts/install_git_hooks.py` once after Git initialization to update and stage the
document automatically before every commit.
