# verify-and-memory

## Purpose

`verify-and-memory` 用于在实现后统一做两件事：

- 验证交付是否真的完成
- 只在合格时提出 memory candidate

## Preconditions

- 已有实际改动结果
- 已有测试结果或明确的未测说明

## Flow

1. 调用 [method-forge-verify-change](../../skills/method-forge-verify-change/SKILL.md)。
2. 产出 `verify.md`，记录行为、测试、风险、文档同步和最终状态。
3. 当 `memory_candidate=yes` 时，只整理候选结论，不直接写长期 memory。
4. 当 `final_status` 不是 `passed` 时，明确阻塞项并回到实现或文档修订。

可选扩展：

- 高风险改动可在步骤 1 之前先运行 `method-forge-code-review`
- 当 `memory_candidate=yes` 且需要独立候选文档时，可在步骤 3 之后运行 `method-forge-memory-promote`

## Memory Candidate Rule

只有同时满足以下条件，才允许在 `verify.md` 中标记候选：

- 已验证
- 可复用
- 稳定
- 可压缩
- 对当前或跨 workspace 的工作方式有帮助

## Exit Criteria

- 已明确是否可交付
- 已明确是否需要后续跟进
- 已明确是否值得提出 memory candidate

## Boundaries

- 不直接写 memory system
- 不替代 code review、diff review 或 PR 流
- 不把“我觉得应该没问题”当作验证证据
