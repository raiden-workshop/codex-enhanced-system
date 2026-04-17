# memory system

这是 Codex App 全局记忆系统的独立工作区。

这里专门维护：

- 全局记忆系统的设计
- 记忆提取、压缩、Dream 整理的实现
- `global / workspace / worker-run` 作用域规则
- 记忆系统相关测试与 QA 文档

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

当前工作区对应的 workspace 记忆节点是：

- `~/.codex/memory/workspaces/memory-system-<workspace-key>/`

全局运行入口是：

```bash
python3 ~/.codex/scripts/refresh_memory.py --workspace-root "$(git rev-parse --show-toplevel)"
```

本工作区里的实现源码当前保存在：

- `scripts/refresh_strict_original_memory.py`
- `tests/test_refresh_strict_original_memory.py`

后续如果继续扩展跨作用域记忆晋升规则，以这里为主，不再放在 `对话` 工作区里继续堆。
