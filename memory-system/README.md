# memory system

这是 `codex-enhanced-system` 里的 Codex App 全局记忆系统子工作区。

这里专门维护：

- 全局记忆系统的设计
- 记忆提取、压缩、Dream 整理的实现
- `global / workspace / worker-run` 作用域规则
- 记忆系统相关测试与 QA 文档

仓库级原生优先边界以根目录 [README.md](../README.md) 里的 `Native-first compatibility map` 为准。

这里维护的是受治理的长期记忆层 `~/.codex/memory/`，不是 Codex App 原生 memories 的实现本体。原生 memories 使用 `~/.codex/memories/`，现在默认承接个人偏好、常见修正和便捷 recall；repo 规则、项目事实、可复用参考和晋升治理仍以本工作区维护的 memory system 为准。

当前默认边界：

- 原生 `~/.codex/memories/` 负责：个人偏好、常见修正、便捷 recall。
- 本工作区的 `~/.codex/memory/` 负责：`project`、`reference`、`open_loop` 以及治理、归档、Dream、promotion。
- 当原生 memories 开启时，旧系统默认关闭 `user` 和 `feedback` 类型，避免双写和重复注入。

这套工作区默认遵循的写作与实现原则是：

- 先想清楚再写
- 简单优先
- 只做必要改动
- 先定义成功标准，再验证结果

正式文档入口：

- `docs/codex-global-memory-system-design.md`
- `docs/codex-global-memory-system-development.md`
- `docs/codex-global-memory-system-alignment.md`
- `docs/codex-global-memory-system-review.md`
- `docs/codex-global-memory-system-qa.md`

当前工作区接入的全局记忆根目录是：

- `~/.codex/memory/`

原生 Codex memories 不在本工作区直接维护：

- `~/.codex/memories/`

当前 workspace 对应的记忆节点需要先通过 `~/.codex/memory/workspaces/index.json` 按 workspace path 查找；节点形态是：

- `~/.codex/memory/workspaces/<mapped-workspace-key>/`

全局运行入口是：

```bash
python3 ~/.codex/scripts/refresh_memory.py --workspace-root "$(git rev-parse --show-toplevel)"
```

本工作区里的实现源码当前保存在：

- `scripts/refresh_strict_original_memory.py`
- `tests/test_refresh_strict_original_memory.py`

后续如果继续扩展跨作用域记忆晋升规则，以这里为主，不再放在 `对话` 工作区里继续堆。
