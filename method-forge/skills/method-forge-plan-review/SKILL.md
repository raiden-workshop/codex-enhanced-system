---
name: method-forge-plan-review
description: Use when reviewing plan.md for risk, gaps, and ordering before tasks are split.
---

# method-forge-plan-review

## Purpose

对 `plan.md` 做质量门审查，优先暴露风险、遗漏和顺序问题。

## Use When

- `plan.md` 刚完成
- 需要判断能否进入任务拆分和实现

## Inputs

- `spec.md`
- `plan.md`
- 仓库约束与现有规则

## Output

- `plan-review.md`
- 模板来源：[docs/templates/plan-review-template.md](../../docs/templates/plan-review-template.md)

## Procedure

1. 先检查计划是否真正覆盖了 spec 的目标与约束。
2. 列出 blocking findings，再看缺失测试和歧义。
3. 检查是否有过度设计或顺序错误。
4. 给出明确结论：`approved` 或 `needs-revision`。

## Completion Standard

- 审批状态明确
- 后续执行者知道是继续拆任务还是回退改 plan

## Guardrails

- Findings 必须优先于摘要
- 不因为“文档已经很完整”就跳过缺失测试检查
- 不把小问题夸大成阻塞，也不把阻塞问题写成建议项

## Handoff

- `approved` 时交给 `method-forge-task-breakdown`
- `needs-revision` 时回到 `method-forge-plan-write`
