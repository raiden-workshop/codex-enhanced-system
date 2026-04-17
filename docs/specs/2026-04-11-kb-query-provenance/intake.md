# Intake / Intake

## Request Summary / 请求摘要

- request: 用户在完成规划后要求“开始落地代码”，当前第一批实现聚焦 `knowledge-base` 的 query 与 provenance 能力。
- request_en: After planning was finalized, the user requested to start implementation; the first implementation slice focuses on `knowledge-base` query and provenance capabilities.
- requester: `user`
- workspace: `<repo-root>`
- date: `2026-04-11`

## Classification / 分类

| Field | Value |
| --- | --- |
| task_type | `complex-change` |
| risk_level | `medium` |
| need_spec | `true` |
| need_research | `false` |
| need_memory_lookup | `false` |
| suggested_path | `spec-flow` |
| next_step | implement `kb query`, docs, and verification |

## Goal / 目标

- primary_goal: 让知识库先具备一个可用的查询入口，并把 `source_refs` / `related` 作为第一层 provenance 暴露出来。
- primary_goal_en: Give the knowledge base a usable query entry point and expose `source_refs` / `related` as the first layer of provenance.
- success_signal: 可以直接运行 `python3 /Users/wz/project/knowledge-base/kb query ...` 拿到排序结果、摘要片段和出处字段。
- success_signal_en: `python3 /Users/wz/project/knowledge-base/kb query ...` returns ranked results, snippets, and provenance fields.

## Constraints And Signals / 约束与信号

- hard_constraints: 不引入外部依赖；保留 `raw/` 与 `wiki/` 的现有边界；不破坏现有命令。
- hard_constraints_en: No new external dependencies; preserve the current `raw/` and `wiki/` boundary; do not break existing commands.
- dependencies: 现有 `/Users/wz/project/knowledge-base/kb` CLI、canonical page frontmatter、`source_refs` 与 `related` 字段。
- dependencies_en: The existing `/Users/wz/project/knowledge-base/kb` CLI, canonical page frontmatter, and the `source_refs` / `related` fields.
- known_risks: 前端没有统一 query contract；现有 `related` 字段存在无后缀短引用，解析时需要兼容。
- known_risks_en: There is no existing query contract yet; current `related` fields use extensionless shorthand references that must be resolved compatibly.

## Reasoning / 判断依据

### Why This Task Type / 为什么是复杂变更

- 需要同时改 CLI、引用解析、命令文档和测试，属于跨文件行为变更。
- This touches CLI behavior, reference resolution, command docs, and tests, so it is a cross-file behavioral change.

### Why This Risk Level / 为什么是中风险

- 风险主要在于误改现有 frontmatter 引用语义，导致维护命令或 provenance 输出失真。
- The main risk is changing existing frontmatter reference semantics in a way that distorts maintenance commands or provenance output.

### Research Or Memory Notes / 研究与记忆说明

- 本轮不再继续 research；直接实现前面规划过的第一批高价值切片。
- No additional research is required in this round; implement the first high-value slice that was already planned.
