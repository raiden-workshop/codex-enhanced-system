---
name: method-forge-memory-promote
description: Use when promoting a verified memory candidate into a more stable memory-candidate.md.
---

# method-forge-memory-promote

## Purpose

把 `verify.md` 中已经通过的 memory candidate 整理成更稳定、可压缩的候选文档，但不直接写入 memory system。

## Use When

- `verify.md` 已标记 `memory_candidate=yes`
- 需要把候选结论交给后续 memory 流程或人工确认

## Inputs

- `verify.md`
- 相关 `spec.md`、`plan.md`
- 可选 `code-review.md`

## Output

- `memory-candidate.md`
- 模板来源：[docs/templates/memory-candidate-template.md](../../docs/templates/memory-candidate-template.md)

## Procedure

1. 从 `verify.md` 提取已验证、可复用、可压缩的最小结论。
2. 删除一次性任务细节、情绪化表述和未验证推断。
3. 建议候选作用域：`workspace`、`global` 或 `none`。
4. 明确说明为什么当前只保留为 candidate。

## Completion Standard

- 候选文档可以被后续 memory 流程消费
- 结论足够短、稳、可复用

## Guardrails

- 不直接写 memory system
- 不把原始分析全文复制进候选文档
- 如果结论还不稳定，宁可给出 `suggested_scope=none`

## Handoff

- 保持 `promotion_status=candidate-only`
- 后续是否真正晋升，由 memory system 既有流程决定
