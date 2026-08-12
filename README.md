# MicroCode 🐣

> A coding agent growing in the open: observable steps, explainable decisions, and replayable history. ✨

[简体中文](README.zh-CN.md) · [Product requirements](doc/prd.md) · [Roadmap](doc/plan.md) · [Architecture](doc/infrastructure.md) · [Progress](doc/进度.md)

MicroCode is a Python command-line coding agent. Its goal is not only to complete a task, but also to make every context choice, model call, tool execution, and permission decision observable, explainable, and replayable.

The project uses an event-sourced architecture and is being built incrementally across milestones M0–M12. The project scaffold and domain event model are complete, but MicroCode is still in early development and is not yet a full coding assistant.

## 🌟 What we are building

- 👀 **Observable** — trace context, model, tool, and approval stages for every turn.
- 💡 **Explainable** — answer why a file, instruction, or memory was selected.
- ⏪ **Replayable** — rebuild history from the Event Log without calling models or tools again.
- 🛡️ **Controlled side effects** — prepare, review, approve, and revalidate mutations.
- 🧠 **Evidence-linked memory** — preserve sources, confidence, and supersession history.
- 🧪 **Offline-testable core** — verify deterministic behavior with scripted providers.

## 🚦 Project status

| Milestone | Status | Scope |
|---|---|---|
| M0 | ✅ Complete | Python scaffold, quality tooling, and architecture automation |
| M1 | ✅ Complete | Strict JSON types, event envelopes, event factory, and Payload Registry |
| M2 | 🛠️ Up next | JSONL Journal and Artifact Store |
| M3–M12 | 🌱 Planned | Sessions, providers, agent loop, tools, CLI, memory, and evaluation |

See [`doc/进度.md`](doc/进度.md) for the latest delivery notes and [`doc/plan.md`](doc/plan.md) for the complete implementation path.

## 🎁 What works today

- 27 consistently named MVP domain events.
- An immutable, extra-field-forbidden, UTC-only `EventEnvelope`.
- Strict JSON validation that rejects `Path`, arbitrary Python objects, non-string keys, and non-finite floats.
- An event factory that requires an explicit `stream_version`.
- A `PayloadRegistry` with known-event validation and unknown-event diagnostic mode.
- A runnable CLI scaffold and automated M1 contract tests.

## 🚀 Quick start

Python 3.11 or newer is required. The following example uses Windows PowerShell:

```powershell
cd D:\vscode\projects\codeDemo\MicroCode
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Verify the installation:

```powershell
microcode --version
microcode --help
```

The CLI currently validates the project entry point. The interactive agent will arrive in later milestones.

## 🧪 Development checks

```powershell
pytest -m "not integration"
ruff check src tests
ruff format --check src tests
mypy src
python scripts/update_infrastructure.py --check
```

[`doc/infrastructure.md`](doc/infrastructure.md) is generated from the repository tree and Python module docstrings. After changing source, tests, configuration, or documentation, run:

```powershell
python scripts/update_infrastructure.py
python scripts/update_infrastructure.py --check
```

## 🗺️ Design map

```text
CLI → Runtime → Agent Loop
                 ├─ Context Compiler
                 ├─ Provider Protocol
                 └─ Tool Pipeline → Policy → Approval → Executor

Runtime → Event Journal → Projection / Trace / Replay
```

The central rule is simple: **the Event Log is the source of truth, projections are rebuildable, and replay never causes side effects.**

## 📦 Local data

Future sessions, events, artifacts, snapshots, and memories will live under `~/.microcode`, never inside the project being operated on. API keys are read only from environment variables or user-level configuration and are never written to the Event Log.

## 🤝 Join the fun

MicroCode is designed to be learned, implemented, and verified one milestone at a time. Pick the next step from [`doc/plan.md`](doc/plan.md), open an issue, or send a pull request. Before contributing, review the [development checks](#-development-checks) and the repository-level `AGENTS.md`.

If you enjoy making agent behavior easier to understand, come help this little agent grow. 🌈

## 📄 License

MicroCode is available under the [MIT License](LICENSE).
