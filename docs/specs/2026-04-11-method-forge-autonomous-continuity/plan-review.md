# Plan Review / 计划复核

## Review / 复核

- 这是语义约束缺口，不是实现引擎 bug，因此应优先修文档真相源和消费方规则。
- 同步消费方 AGENTS 很重要，否则 method-forge 自己修了，实际工作区仍可能继续按旧习惯停下来。
- 不需要发明新状态，只需要把 `running` 与 `completed` 的使用边界写清楚。

- This is a semantic-constraint gap rather than an engine bug, so the source-of-truth docs and consumer rules should be fixed first.
- Syncing consumer AGENTS matters; otherwise method-forge can be fixed while actual workspaces still stop under the old habit.
- No new status is needed; the important part is clarifying how `running` and `completed` should be used.
