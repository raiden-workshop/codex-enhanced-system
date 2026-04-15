# Intake

## Request Summary

- request: 为 `method-forge` 补齐 orchestration 文档，并在根 `README.md` 里加入入口说明，确保新 worker 知道如何从 intake 走到 verify。
- requester: workspace bootstrap
- workspace: `<repo-root>/method-forge`
- date: `2026-04-10`

## Classification

| Field | Value |
| --- | --- |
| task_type | `complex-change` |
| risk_level | `medium` |
| need_spec | `true` |
| need_research | `false` |
| need_memory_lookup | `true` |
| suggested_path | `spec-flow` |
| next_step | 先产出 `spec.md`，再进入完整文档流。 |

## Goal

- primary_goal: 让新 worker 能从入口 orchestration 明白标准流程和收尾验证方式。
- success_signal: `README.md`、3 个 orchestration 文档和方法规则文档之间的术语、边界和顺序一致。

## Constraints And Signals

- hard_constraints: 必须统一使用 `orchestrations`，不能把会话内流程继续称为 `automations`。
- dependencies: 需要遵守当前环境的 Codex 原生能力边界。
- known_risks: 如果 README 和 orchestration 规则不一致，新 worker 会从入口就走偏。

## Reasoning

### Why This Task Type

- 该请求涉及多个文件和流程定义，不适合直接边写边定规则。

### Why This Risk Level

- 风险不在运行时，而在方法层漂移；一旦术语和边界写错，后续所有 worker 都会继承错误。

### Research Or Memory Notes

- 需要查当前环境最新规则，确认 `automations` 与 `orchestrations` 的命名边界。
