# method-forge-code-review

## Purpose

对已完成的实现做专注于正确性、回归风险和遗漏测试的质量审查。

## Use When

- 高风险改动完成后
- `verify-change` 前需要额外质量门时
- 用户明确要求 review 时

## Inputs

- 实际改动结果
- `spec.md`
- `plan.md`
- `tasks.md`
- 测试结果
- 相关 diff 或文件上下文

## Output

- `code-review.md`
- 模板来源：[docs/templates/code-review-template.md](../../docs/templates/code-review-template.md)

## Procedure

1. 先看是否偏离 `spec` 与 `plan`。
2. 以 finding 为主，按严重性排序记录问题。
3. 检查遗漏测试、边界条件与回归风险。
4. 若无 findings，也要说明残余风险或覆盖盲区。
5. 给出 `review_status`，用于决定是否回到实现。

## Completion Standard

- 审查结论能明确指导是继续 verify 还是先修问题
- findings 具备足够具体的文件/行为上下文

## Guardrails

- 不复制 Codex 原生 diff review 面板
- 不把风格偏好写成阻塞问题
- findings 必须优先于摘要

## Handoff

- `review_status=needs-fix` 时回到实现
- `review_status=approved` 或 `advisory-only` 时把结论作为 `verify-change` 输入
