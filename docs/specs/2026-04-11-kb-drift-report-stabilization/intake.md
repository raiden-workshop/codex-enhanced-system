# Intake / 需求摄取

## Request / 请求

- 用户继续要求推进实现。
- The user asked to continue advancing the implementation.

## Problem / 问题

- `kb drift-review --write-report` 之前按写入前的 signals 直接渲染报告。
- 这会导致命令本身刚刚解决掉的 `report-lag` 仍然被写进新报告里，形成一次需要手工回写的“旧快照”。

- `kb drift-review --write-report` previously rendered the report directly from the pre-write signals.
- That meant the command could archive the very `report-lag` it had just resolved, leaving a stale snapshot that required manual cleanup.

## Scope / 范围

- 收敛 drift-review report 的写回语义
- 保持真实仓库的 stable/healthy 状态不被打破
- 补回归测试和双语文档

- Stabilize the drift-review report writeback semantics
- Preserve the real repository's stable/healthy state
- Add regression coverage and bilingual docs
