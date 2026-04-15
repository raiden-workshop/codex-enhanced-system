# Intake / 需求摄取

## Request / 请求

- 用户继续要求推进实现。
- The user asked to keep the implementation moving.

## Problem / 问题

- 前一刀已经把 command-generated report 的 index 收口做齐了，但 `reindex` 和 `delete` 仍然可能在改写 `wiki/index.md` 后不更新 `updated_at`。
- 这会让 index 内容已变、metadata 仍旧的情况继续存在。

- The previous slice already closed index registration for command-generated reports, but `reindex` and `delete` could still rewrite `wiki/index.md` without refreshing `updated_at`.
- That leaves a state where the index content changes while the metadata still looks stale.

## Scope / 范围

- 让 `reindex` 在实际改写 index 时刷新 `updated_at`
- 让删除路径移除 index 条目时也刷新 `updated_at`
- 补测试、文档和双语变更包

- Make `reindex` refresh `updated_at` when it actually rewrites the index
- Make the delete path refresh `updated_at` when it removes index entries
- Add tests, docs, and a bilingual change package
