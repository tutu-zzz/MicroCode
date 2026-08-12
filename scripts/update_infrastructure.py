"""Generate doc/infrastructure.md from the repository tree and module docstrings."""

from __future__ import annotations

import argparse
import ast
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "doc" / "infrastructure.md"

IGNORED_DIRECTORIES = {
    ".agents",
    ".codex",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp",
    ".venv",
    "__pycache__",
    "build",
    "dist",
}
IGNORED_SUFFIXES = {".pyc", ".pyo"}

ROLE_OVERRIDES = {
    ".githooks/pre-commit": "提交前自动重建并暂存项目架构文档。",
    ".gitignore": "定义虚拟环境、缓存、构建产物和本地密钥文件的忽略规则。",
    "AGENTS.md": "约束后续开发和 Agent 在每次改动后同步生成架构文档。",
    "LICENSE": "项目的 MIT 开源许可证。",
    "README.md": "英文项目入口，提供定位、安装和开发检查说明。",
    "README.zh-CN.md": "中文项目入口，提供定位、安装和开发检查说明。",
    "doc/infrastructure.md": "当前文件；由脚本生成的项目架构、文件清单和维护规则。",
    "doc/plan.md": "从 M0 到 M12 的 MVP 逐步实现教程。",
    "doc/prd.md": "定义产品目标、MVP 边界、核心创新和验收标准。",
    "pyproject.toml": "定义 Python 包元数据、依赖、CLI 入口和质量工具配置。",
    "scripts/install_git_hooks.py": "为当前 Git 仓库启用已提交的 .githooks 目录。",
    "scripts/update_infrastructure.py": "扫描项目并确定性生成本架构文档。",
    "tests/fixtures/README.md": "说明脱敏 Provider fixture 和临时项目模板的存放规则。",
    "tests/golden/README.md": "说明 Golden Trace 场景及其预期产物。",
    "tests/integration/README.md": "说明需要真实 Provider 或外部程序的集成测试规则。",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when doc/infrastructure.md does not match the generated content.",
    )
    return parser.parse_args()


def should_include(path: Path) -> bool:
    relative = path.relative_to(PROJECT_ROOT)
    if not path.is_file():
        return False
    if any(part in IGNORED_DIRECTORIES for part in relative.parts):
        return False
    if path.suffix in IGNORED_SUFFIXES or path.name.endswith(".egg-info"):
        return False
    return True


def discover_files() -> list[Path]:
    return sorted(
        (path for path in PROJECT_ROOT.rglob("*") if should_include(path)),
        key=lambda path: path.relative_to(PROJECT_ROOT).as_posix().casefold(),
    )


def module_docstring(path: Path) -> str | None:
    try:
        module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return None
    docstring = ast.get_docstring(module, clean=True)
    if not docstring:
        return None
    return docstring.splitlines()[0].strip()


def markdown_title(path: Path) -> str | None:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line.removeprefix("# ").strip()
    except (OSError, UnicodeDecodeError):
        return None
    return None


def describe_file(path: Path) -> str:
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    if relative in ROLE_OVERRIDES:
        return ROLE_OVERRIDES[relative]
    if path.suffix == ".py":
        return module_docstring(path) or "Python 模块；请补充模块 docstring 说明职责。"
    if path.suffix == ".md":
        title = markdown_title(path)
        return f"文档：{title}。" if title else "项目文档。"
    if path.suffix == ".toml":
        return "TOML 配置文件。"
    return "项目文件；如职责特殊，请在生成脚本的 ROLE_OVERRIDES 中补充。"


def status_for(path: Path) -> str:
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    if relative == "doc/infrastructure.md":
        return "自动生成"
    if relative.startswith("tests/"):
        return "测试/Fixture"
    if relative.startswith(".githooks/") or relative.startswith("scripts/"):
        return "开发自动化"
    if path.suffix == ".md" or path.name == "LICENSE":
        return "文档"
    if path.suffix in {".toml", ".gitignore"} or path.name == ".gitignore":
        return "配置"
    if path.suffix == ".py":
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return "Python 模块"
        return "架构骨架" if "NotImplementedError" in source else "基础实现"
    return "项目文件"


def inventory_fingerprint(files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        if relative == "doc/infrastructure.md":
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()[:16]


def brief_description(path: Path) -> str:
    """Return a compact one-line role suitable for the architecture tree."""

    description = " ".join(describe_file(path).split())
    return description.rstrip("。.")


def build_tree(files: list[Path]) -> str:
    tree: dict[str, object] = {}
    for path in files:
        node = tree
        parts = path.relative_to(PROJECT_ROOT).parts
        for part in parts[:-1]:
            child = node.setdefault(part, {})
            if not isinstance(child, dict):
                raise ValueError(f"file/directory collision at {part}")
            node = child
        node[parts[-1]] = path

    lines = ["MicroCode/"]

    def emit(node: dict[str, object], prefix: str) -> None:
        entries = sorted(
            node.items(),
            key=lambda item: (0 if isinstance(item[1], dict) else 1, item[0].casefold()),
        )
        for index, (name, child) in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = "└── " if is_last else "├── "
            if isinstance(child, dict):
                lines.append(f"{prefix}{connector}{name}/")
                emit(child, prefix + ("    " if is_last else "│   "))
            else:
                if not isinstance(child, Path):
                    raise TypeError(f"unexpected tree node for {name}: {type(child)!r}")
                lines.append(
                    f"{prefix}{connector}{name} — {brief_description(child)}"
                )

    emit(tree, "")
    return "\n".join(lines)


def escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_file_tables(files: list[Path]) -> str:
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        relative = path.relative_to(PROJECT_ROOT)
        group = relative.parent.as_posix() if relative.parent.as_posix() != "." else "项目根目录"
        groups[group].append(path)

    sections: list[str] = []
    for group in sorted(groups, key=lambda value: (value != "项目根目录", value.casefold())):
        sections.extend(
            [
                f"### `{group}`",
                "",
                "| 文件 | 当前状态 | 作用 |",
                "|---|---|---|",
            ]
        )
        for path in groups[group]:
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            sections.append(
                f"| `{escape_table(relative)}` | {status_for(path)} | "
                f"{escape_table(describe_file(path))} |"
            )
        sections.append("")
    return "\n".join(sections).rstrip()


def render_document(files: list[Path]) -> str:
    fingerprint = inventory_fingerprint(files)
    tree = build_tree(files)
    tables = render_file_tables(files)
    return f"""# MicroCode 项目架构说明

> 本文档由 `scripts/update_infrastructure.py` 自动生成，请勿直接编辑。
>
> 项目清单指纹：`{fingerprint}`
>
> 更新命令：`python scripts/update_infrastructure.py`

## 1. 文档目的

本文档描述 MicroCode 当前项目分层、文件树、每个文件的职责和文档自动更新机制。它反映的是当前工作区实际状态；产品目标见 `doc/prd.md`，逐步实现教程见 `doc/plan.md`。

“架构骨架”表示文件和接口已经建立，但仍包含明确的 `NotImplementedError`；“基础实现”表示已经有可执行逻辑，但不等于对应 MVP 里程碑已经验收完成。

## 2. 架构原则

1. Event Log 是会话、审批、工具结果和记忆的唯一事实源。
2. CLI 只负责输入输出，不持有业务状态。
3. Agent Loop 只编排上下文、Provider 和工具流水线。
4. 副作用统一经过 `validate → prepare → policy → approval → execute → record`。
5. Projection 和 Snapshot 可以重建，Replay 不调用模型、不执行工具。
6. Python 模块的首行 docstring 是本文件职责说明的默认来源。

## 3. 分层与依赖

```mermaid
flowchart TD
    CLI["cli · 输入与渲染"] --> Runtime["runtime · 组合与应用服务"]
    Runtime --> Agent["agent · 有界 Agent Loop"]
    Agent --> Context["context · 上下文编译"]
    Agent --> Provider["provider · 模型协议与适配器"]
    Agent --> Tools["tools · 工具注册与准备"]
    Tools --> Actions["actions · PreparedAction 与执行"]
    Actions --> Policy["policy · allow / ask / deny"]
    Runtime --> EventLog["eventlog · Journal / Artifact / Replay"]
    EventLog --> Session["session · 可重建会话投影"]
    Context --> Memory["memory · 证据化记忆"]
    Session --> Domain["domain · 事件与消息类型"]
    Provider --> Domain
    Tools --> Domain
```

依赖方向应由外层适配器指向内层协议和领域模型。`domain` 不得引用 CLI、厂商 SDK 或具体存储实现；Replay 不得依赖 Provider 和 Tool Executor。

### 3.1 运行时数据流

```mermaid
flowchart LR
    U["用户输入"] --> C["CLI 主对话区"]
    C --> R["Runtime"]
    R --> A["Agent Loop"]
    A --> X["Context Compiler"]
    X --> P["Provider"]
    P --> A
    A --> T["Tool Pipeline"]
    T --> A
    R --> J["Event Journal"]
    R --> N["Runtime Notification"]
    N --> V["Progress Panel Model"]
    V --> S["CLI 进度侧栏"]
    J --> Q["Session / Trace / Replay"]
```

Event Journal 保存可重建的业务事实；Runtime Notification 用于即时渲染，Progress Panel Model 只投影当前 Turn 的轻量阶段状态。两条路径都不允许由 CLI 反向修改领域状态。

## 4. 当前文件架构

每个文件名后直接列出简要职责；更完整的职责与实现状态见第 5 节。

```text
{tree}
```

## 5. 文件作用说明

{tables}

## 6. 运行时数据位置

生成状态不写入被操作项目，默认位于：

```text
~/.microcode/
├── events/       # Session 与 Memory 事件流
├── artifacts/    # SHA-256 内容寻址的大输出
├── snapshots/    # 可删除、可重建的投影缓存
├── locks/        # Event stream 文件锁
└── settings.json # 非领域 UI 偏好
```

被操作的项目只允许共享 `AGENTS.md`、`MICRO.md` 和可选 `.microcode/config.toml`。

## 7. 自动更新机制

架构文档采用三层保障：

1. **生成器**：`python scripts/update_infrastructure.py` 扫描文件树、读取 Python module docstring、计算项目指纹并重写本文档。
2. **测试守卫**：`tests/unit/test_infrastructure_doc.py` 使用 `--check` 验证本文档与当前项目完全一致；过期时测试失败。
3. **提交钩子**：运行一次 `python scripts/install_git_hooks.py` 后，`.githooks/pre-commit` 会在每次提交前自动生成并暂存本文档。

项目根目录的 `AGENTS.md` 还要求所有后续 Agent/开发任务在交付前运行生成与检查命令。

### 新增或修改文件时

- Python 文件：更新模块顶部 docstring，生成器自动把它作为职责说明。
- 非 Python 文件：通用文件会自动获得默认说明；特殊职责在生成脚本的 `ROLE_OVERRIDES` 中补充。
- 新增、删除、移动或修改任意纳入扫描的文件：项目清单指纹都会变化，必须重新生成本文档。

### 手工验证

```powershell
python scripts/update_infrastructure.py
python scripts/update_infrastructure.py --check
```
"""


def main() -> int:
    args = parse_args()
    files = discover_files()
    if OUTPUT_PATH not in files:
        files.append(OUTPUT_PATH)
        files.sort(key=lambda path: path.relative_to(PROJECT_ROOT).as_posix().casefold())
    expected = render_document(files)

    if args.check:
        actual = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if actual != expected:
            print(
                "doc/infrastructure.md is stale; run "
                "`python scripts/update_infrastructure.py`.",
                file=sys.stderr,
            )
            return 1
        print("doc/infrastructure.md is up to date")
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="\n")
    print(f"updated {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
