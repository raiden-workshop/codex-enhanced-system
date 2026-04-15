# Codex Global Memory System Review

日期：2026-04-03

## 结论

本轮实现没有发现阻塞上线的代码问题。

已经补齐并验证的关键点：

- `worker-run` 运行态已落盘到 `runs/<workspace-key>/<run-id>/`
- `user` 记忆改为先落 `workspace candidates`，再由 `global dream` 提升
- `global dream` 有了独立触发配置，不再只能跟着 workspace dream 逻辑走
- `global conflict queue` 能识别跨 workspace 的相反全局规则
- `global dream` 会把不再满足晋升条件的 `global active` 条目标为 `stale`
- `reference` 的全局晋升被收紧，避免单 workspace 高分参考直接污染全局层
- 历史 workspace 记忆现在会自动回填 `source_workspaces` / `source_runs`
- `global candidates` 现在有 promoted / duplicate / expired / overflow 归档治理
- 已经用真实新 run 验证过 `session -> runs -> workspace memory -> active_context` 整链路

## 已解决的问题

1. 旧实现里 `user` 记忆仍按 workspace active 验证，和新架构不一致。
   现在测试与实现都改成了 `workspace candidate -> global active`。

2. `global conflict queue` 的聚合结构最初只编译通过，但冲突场景下会丢失正确分组。
   现在改成按主题和 polarity 扁平聚合，并补了跨 workspace 冲突测试。

3. `global dream` 之前只会新增，不会把不再满足条件的 global 记忆降级。
   现在会把失去资格的 global active 标记为 `stale`。

4. 全局 reference 晋升过宽。
   现在要求更严格的跨 workspace 证据，并过滤明显的 assistant meta 话术。

## 剩余风险

1. 历史复制出来的 workspace 记忆，即使完成了保守迁移，也仍可能让“真实跨项目重复”被低估。
   这是当前策略的有意取舍：宁可少晋升，也不要把复制历史误判成全局共识。

2. `global dream` 在证据消失时会把不再满足条件的 global active 降级成 `stale`。
   这能保持全局层干净，但如果未来需要“证据暂时缺席也保留 active”的策略，还需要再设计 retention 规则。
