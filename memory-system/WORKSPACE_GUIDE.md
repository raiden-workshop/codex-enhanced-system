# memory system Workspace Guide

当前工作区是 `codex-enhanced-system` 里的 Codex App 全局记忆系统子工作区。

约定：

- 全局记忆根目录是 `~/.codex/memory/`
- 当前 workspace 节点必须先通过 `~/.codex/memory/workspaces/index.json` 按 workspace path 查找；不要硬编码 workspace key。
- 设计、实现、测试、QA 都在这个工作区维护
- 开始复杂任务前，先读：
  - `~/.codex/memory/instructions/company/GUIDE.md`
  - `~/.codex/memory/instructions/user/GUIDE.md`
  - `~/.codex/memory/instructions/local/GUIDE.md`
  - `~/.codex/memory/workspaces/<mapped-workspace-key>/instructions/repo/GUIDE.md`
  - `~/.codex/memory/workspaces/<mapped-workspace-key>/memories/MEMORY.md`
  - `~/.codex/memory/workspaces/<mapped-workspace-key>/runtime/active_context.md`
- 完成重要任务后，运行：
  - `python3 ~/.codex/scripts/refresh_memory.py --workspace-root "$(git rev-parse --show-toplevel)"`
