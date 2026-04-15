# Failure And Rework Rules

## 1. 目的

`method-forge v1.5` 为 workflow 增加统一的失败回退规则，避免流程在失败后分叉出第二套真相源。

核心原则：

- 失败后优先修订原文档，不另开平行文档
- 阻塞点要写清楚，不能只写“后续处理”
- 回退路径要固定，让下一个执行者知道从哪里继续

## 2. 失败类型与回退路径

| Failure Type | 典型信号 | 必须回到哪里 |
| --- | --- | --- |
| intake 不稳定 | `next_step` 无法确定，目标仍含糊 | 回到 `intake.md` |
| spec 不稳定 | `open_questions` 阻塞核心目标 | 回到 `spec.md` |
| plan 被拒 | `plan-review.approval_status=needs-revision` | 回到 `plan.md` |
| task 粒度不对 | 任务无法独立执行或验证 | 回到 `tasks.md` |
| 实现偏离 plan | 触点、顺序或范围明显漂移 | 回到 `plan.md`，必要时同步 `spec.md` |
| code review 发现阻塞问题 | 正确性、回归或缺失测试问题成立 | 回到实现，再补 `code-review.md` |
| verify 未通过 | 行为、测试、文档或风险未达标 | 回到实现或相关文档 |
| memory candidate 不合格 | 结论不稳定、不可压缩或未验证 | 保留在 `verify.md`，不要晋升 |

## 3. 单一真相源规则

- `intake` 的真相源是 `intake.md`
- 需求边界的真相源是 `spec.md`
- 技术方案的真相源是 `plan.md`
- 计划审查结论的真相源是 `plan-review.md`
- 执行拆解的真相源是 `tasks.md`
- 交付验收的真相源是 `verify.md`
- 增强审查的真相源是 `code-review.md`
- memory 候选整理的真相源是 `memory-candidate.md`

回退时应更新原真相源，而不是新开 `plan-v2-final-final.md` 之类的漂移文件。

## 4. 回退动作要求

每次失败回退都至少补这 3 项：

- blocking reason
- next owner
- next re-entry point

推荐写法：

```text
blocking_reason: plan misses rollback path for data migration
next_owner: plan-write
re_entry_point: update plan.md, then rerun plan-review
```

## 5. 人工确认边界

以下情况建议暂停并做人类确认：

- `spec.md` 的目标或范围发生实质变化
- `plan.md` 为通过 review 而不得不改动核心实现路径
- `verify.md` 显示行为达标但测试证据不足
- memory candidate 可能覆盖现有稳定规则

## 6. 不允许的回退方式

- 失败后跳过前置文档直接继续实现
- 用会话聊天补丁替代文档修订
- 为了赶进度跳过 `plan-review` 或 `verify`
- 把未验证结论直接写成 memory
