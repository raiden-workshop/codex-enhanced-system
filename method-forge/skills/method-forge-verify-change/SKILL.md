# method-forge-verify-change

## Purpose

验证改动是否真正达成目标，并判断是否值得提出 memory candidate。

## Use When

- 任何实质性改动完成后
- 需要回答“是否交付完成”而不只是“是否已经改过文件”

## Inputs

- 实际改动结果
- `spec.md`
- `plan.md`
- `tasks.md`
- 测试结果

对于轻任务，如果没有完整 spec 流，至少要补充：

- `intake.md`
- 与改动直接相关的验证证据

## Output

- `verify.md`
- 模板来源：[docs/templates/verify-template.md](../../docs/templates/verify-template.md)

## Procedure

1. 对照 spec 或 intake 检查行为是否达标。
2. 记录测试结果，而不是只写“应该没问题”。
3. 评估回归风险和文档同步状态。
4. 判断是否存在稳定、可复用、可压缩的 memory candidate。
5. 给出 `final_status`，只能基于证据，不基于乐观预期。

## Completion Standard

- 已明确行为、测试、风险、文档和 memory candidate 的状态
- 团队能够据此判断是否可以交付或还需跟进

## Guardrails

- 不因为改动是文档类就跳过 verify
- 不直接写长期 memory
- 如果测试未运行，要明确写出未验证项和残余风险

## Handoff

- `final_status=passed` 时可以作为交付完成依据
- `memory_candidate=yes` 时只整理候选结论，不直接触发 memory 写入
