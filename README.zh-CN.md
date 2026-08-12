# MicroCode 🐣

> 一个正在认真长大的 Code Agent：过程看得见，决策说得清，历史放得回。✨

[English](README.md) · [产品需求](doc/prd.md) · [开发路线](doc/plan.md) · [项目架构](doc/infrastructure.md) · [开发进度](doc/进度.md)

MicroCode 是一个用 Python 构建的命令行 Code Agent。它不只追求“把任务做完”，还希望让每次上下文选择、模型调用、工具执行与权限决策都可以被观察、解释和回放。

项目采用事件溯源架构，并按照 M0–M12 的里程碑逐步实现。当前已完成工程骨架和领域事件模型，仍处于早期开发阶段，暂时还不是一个功能完整的编码助手。

## 🌟 我们想做什么

- 👀 **可观察**：每个 Turn 的上下文、模型、工具和审批阶段都有迹可循。
- 💡 **可解释**：可以回答“为什么选择这些文件和记忆”。
- ⏪ **可回放**：从 Event Log 重建历史，不重新调用模型或执行工具。
- 🛡️ **副作用可控**：文件修改与命令执行经过准备、策略、审批和校验。
- 🧠 **记忆有证据**：长期记忆保留来源、置信度和替代关系。
- 🧪 **离线可测试**：核心流程优先使用 Scripted Provider 和确定性测试验证。

## 🚦 当前进度

| 里程碑 | 状态 | 内容 |
|---|---|---|
| M0 | ✅ 完成 | Python 工程骨架、质量工具与架构文档自动化 |
| M1 | ✅ 完成 | 严格 JSON 类型、事件信封、事件工厂与 Payload Registry |
| M2 | 🛠️ 下一步 | JSONL Journal 与 Artifact Store |
| M3–M12 | 🌱 规划中 | Session、Provider、Agent Loop、工具、CLI、记忆与 Eval |

详细记录见 [`doc/进度.md`](doc/进度.md)，完整实现路径见 [`doc/plan.md`](doc/plan.md)。

## 🎁 现在已经有什么

- 27 个统一命名的 MVP 领域事件。
- 不可变、禁止额外字段并强制 UTC 时间的 `EventEnvelope`。
- 拒绝 `Path`、任意 Python 对象、非字符串键和非有限浮点数的严格 JSON 校验。
- 显式接收 `stream_version` 的事件工厂。
- 支持已知事件 schema 校验和未知事件诊断模式的 `PayloadRegistry`。
- 可运行的 CLI 骨架与完整的 M1 自动化测试。

## 🚀 快速开始

需要 Python 3.11 或更高版本。下面的命令以 Windows PowerShell 为例：

```powershell
cd D:\vscode\projects\codeDemo\MicroCode
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

确认安装成功：

```powershell
microcode --version
microcode --help
```

目前 CLI 主要用于验证工程入口；交互式 Agent 将在后续里程碑接入。

## 🧪 开发与检查

```powershell
pytest -m "not integration"
ruff check src tests
ruff format --check src tests
mypy src
python scripts/update_infrastructure.py --check
```

架构文档 [`doc/infrastructure.md`](doc/infrastructure.md) 根据项目文件树和 Python 模块 docstring 自动生成。修改源码、测试、配置或文档后运行：

```powershell
python scripts/update_infrastructure.py
python scripts/update_infrastructure.py --check
```

## 🗺️ 设计地图

```text
CLI → Runtime → Agent Loop
                 ├─ Context Compiler
                 ├─ Provider Protocol
                 └─ Tool Pipeline → Policy → Approval → Executor

Runtime → Event Journal → Projection / Trace / Replay
```

核心原则是：**Event Log 是唯一事实源，Projection 可以重建，Replay 不产生副作用。**

## 📦 本地数据

未来生成的 Session、Event、Artifact、Snapshot 和记忆默认保存在 `~/.microcode`，不会写进正在操作的项目。API Key 只从环境变量或用户级配置读取，不会进入 Event Log。

## 🤝 一起玩耍

这是一个边学习、边实现、边验证的项目。欢迎从 [`doc/plan.md`](doc/plan.md) 选择下一个里程碑，也欢迎提交 Issue 或 Pull Request。开始贡献前请先阅读[开发与检查](#-开发与检查)和仓库根目录的 `AGENTS.md`。

如果你也喜欢让 Agent 的“思考轨迹”更清楚，欢迎一起把 MicroCode 养大。🌈

## 📄 License

本项目使用 [MIT License](LICENSE)。
