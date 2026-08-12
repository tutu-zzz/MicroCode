# MicroCode

MicroCode 是一个可观察、可解释、可回放的命令行 Code Agent。

当前仓库处于“架构骨架”阶段。后续按照 [`doc/plan.md`](doc/plan.md) 的 M0–M12 逐步实现，
完整产品需求与 MVP 边界见 [`doc/prd.md`](doc/prd.md)。

## 开发环境

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
microcode --help
```

## 质量检查

```powershell
pytest -m "not integration"
ruff check src tests
ruff format --check src tests
mypy src
```

会话、事件、Artifact 和记忆等生成状态将保存在 `~/.microcode`，不会污染被操作的项目。

## 架构文档

[`doc/infrastructure.md`](doc/infrastructure.md) 根据项目文件树和 Python 模块 docstring 自动生成。
每次开发改动后运行：

```powershell
python scripts/update_infrastructure.py
python scripts/update_infrastructure.py --check
```

初始化 Git 后执行一次 `python scripts/install_git_hooks.py`，即可在每次提交前自动更新并暂存架构文档。
