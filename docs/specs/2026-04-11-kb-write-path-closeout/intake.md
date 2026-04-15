# Intake / 需求摄取

## Request / 请求

- 用户继续要求推进实现。
- The user asked to keep the implementation moving.

## Problem / 问题

- `cmd_log` 追加日志时不会同步刷新 `wiki/log.md.updated_at`。
- `cmd_add` 创建 canonical page 后仍要求手动再跑一次 `reindex --write`，否则新页会立刻处于 “missing from wiki/index.md”。
- `cmd_add` 和 `cmd_delete` 仍然需要再单独补一条结构化 `log`，自动流程不够顺手。

- `cmd_log` appended log entries without refreshing `wiki/log.md.updated_at`.
- `cmd_add` still required a manual `reindex --write` after creating a canonical page, otherwise the new page immediately landed in a “missing from wiki/index.md” state.
- `cmd_add` and `cmd_delete` still required a separate structured `log` step, which kept automated flows from feeling fully smooth.

## Scope / 范围

- 让 `cmd_log` 在实际写入时刷新 `wiki/log.md.updated_at`
- 让 `cmd_add` 创建 canonical page 后自动补入 `wiki/index.md`
- 给 `cmd_add` / `cmd_delete` 增加可选的 `--write-log`
- 补测试、命令文档和双语变更包

- Make `cmd_log` refresh `wiki/log.md.updated_at` on real writes
- Make `cmd_add` auto-register canonical pages in `wiki/index.md`
- Add optional `--write-log` support to `cmd_add` / `cmd_delete`
- Add tests, command docs, and a bilingual change package
