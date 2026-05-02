---
name: method-forge-task-breakdown
description: Use when splitting an approved plan into small executable tasks.md items.
---

# method-forge-task-breakdown

## Purpose

把通过审查的计划拆成小而清晰的 `tasks.md`，让执行与验证都能逐项落地。

## Use When

- `plan-review.md` 已给出 `approved`
- 需要把计划交给主 agent 或后续 worker 执行

## Inputs

- `plan.md`
- `plan-review.md`

## Output

- `tasks.md`
- 模板来源：[docs/templates/tasks-template.md](../../docs/templates/tasks-template.md)

## Procedure

1. 依据 `implementation_order` 切分任务，而不是凭感觉分段。
2. 每个任务至少写清 `id`、`goal`、`files`、`depends_on`、`verification`、`done_definition`。
3. 显式标注依赖和可并行部分。
4. 保持任务粒度足够小，确保能执行、能验证、能回滚。

## Completion Standard

- 每个任务都具备清晰输入和完成定义
- 执行者无需重写计划即可开始工作

## Guardrails

- `plan-review` 未批准时不得继续
- 不把整个计划压成一个“大任务”
- 不省略验证方式

## Handoff

- `tasks.md` 交给实现层执行
- 实现完成后由 `method-forge-verify-change` 做验收闭环
