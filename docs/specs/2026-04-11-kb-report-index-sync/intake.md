# Intake / 需求摄取

## Request / 请求

- 用户继续要求推进实现。
- The user asked to keep the implementation moving.

## Problem / 问题

- `maintain --write-report` 在写入新 report 后会立刻留下 `missing from wiki/index.md` 的维护残留。
- `drift-review --write-report` 也存在同类风险，只是之前靠手工导航收口规避了它。

- `maintain --write-report` immediately left a `missing from wiki/index.md` maintenance residue after writing a new report.
- `drift-review --write-report` carried the same class of risk, even though earlier manual guide updates had masked it.

## Scope / 范围

- 让 report-producing commands 自动同步 `wiki/index.md`
- 保持现有 `stable` / `healthy` 基线不被打破
- 补测试、命令文档和双语变更包

- Make report-producing commands auto-sync `wiki/index.md`
- Preserve the existing `stable` / `healthy` baseline
- Add tests, command docs, and a bilingual change package
