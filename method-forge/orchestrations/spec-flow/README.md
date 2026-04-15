# spec-flow

## Purpose

`spec-flow` 负责编排复杂任务的标准文档流：

```text
spec-clarify
-> plan-write
-> plan-review
-> task-breakdown
```

## Preconditions

- `intake.md` 已存在
- `intake.md.need_spec=true`

## Flow

1. 调用 [method-forge-spec-clarify](../../skills/method-forge-spec-clarify/SKILL.md)，产出 `spec.md`。
2. 对高风险或边界复杂任务，可在 `spec.md` 后暂停确认。
3. 调用 [method-forge-plan-write](../../skills/method-forge-plan-write/SKILL.md)，产出 `plan.md`。
4. 对高风险或顺序敏感任务，可在 `plan.md` 后暂停确认。
5. 调用 [method-forge-plan-review](../../skills/method-forge-plan-review/SKILL.md)，产出 `plan-review.md`。
6. 若 `approval_status=needs-revision`，回到 `plan-write` 修订。
7. 若 `approval_status=approved`，调用 [method-forge-task-breakdown](../../skills/method-forge-task-breakdown/SKILL.md)，产出 `tasks.md`。

## Exit Criteria

- `tasks.md` 已产出
- 执行顺序和依赖关系可直接用于实现

## Failure And Rework Rules

- `spec.md` 仍有阻塞性未决问题时，不得硬进 `plan-write`
- `plan-review.md` 不通过时，不得硬进 `task-breakdown`
- 修订时优先更新原文档，不要另外开平行真相源

## Boundaries

- 不直接写代码
- 不跳过 `plan-review`
- 不把编排层做成后台自动任务或审批系统
