# Tasks

## Task List

### T1

- id: `T1`
- goal: 写 `docs/method/orchestration-rules.md`，固定全局编排规则和术语修正。
- files:
  - `<repo-root>/method-forge/docs/method/orchestration-rules.md`
  - `<repo-root>/method-forge/docs/method/codex-native-boundaries.md`
- depends_on: `none`
- verification: 顺读文档，确认明确区分 `orchestrations` 和 Codex 原生 `automations`。
- done_definition: 总规则和边界文档对 `route-request`、`spec-flow`、`verify-and-memory` 的职责描述一致。

### T2

- id: `T2`
- goal: 写 3 个 orchestration README，明确每条路径的目标、顺序、停点和边界。
- files:
  - `<repo-root>/method-forge/orchestrations/route-request/README.md`
  - `<repo-root>/method-forge/orchestrations/spec-flow/README.md`
  - `<repo-root>/method-forge/orchestrations/verify-and-memory/README.md`
- depends_on: `T1`
- verification: 检查每个 README 是否都包含 purpose、flow 和 boundaries。
- done_definition: 新 worker 可以单独打开任一 orchestration README 并知道它在整条流程中的位置。

### T3

- id: `T3`
- goal: 更新根 `README.md`，加入入口导航和标准流程说明。
- files:
  - `<repo-root>/method-forge/README.md`
- depends_on: `T2`
- verification: 顺读 `README.md` 到 3 个 orchestration README 是否形成闭环。
- done_definition: 根 README 只负责导航，不重复细则，且能把读者引导到正确文档。

## Dependency Summary

- `T1 -> T2 -> T3`

## Execution Notes

- sequencing_notes: 先定规则，再写路径，最后写入口。
- parallelism_notes: `T2` 中 3 个 orchestration 文档可以共享结构，但仍以统一规则为前提。
- rollback_notes: 如果路径说明与总规则冲突，优先修订路径说明并保持总规则为真相源。
