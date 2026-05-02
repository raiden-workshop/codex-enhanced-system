---
name: method-forge-plan-write
description: Use when turning spec.md into an executable implementation plan.md.
---

# method-forge-plan-write

## Purpose

把 `spec.md` 变成可执行的技术实现方案 `plan.md`。

## Use When

- `spec.md` 已稳定
- 已有足够仓库上下文来判断触点、顺序与风险

## Inputs

- `spec.md`
- 代码库或文档库上下文
- 相关 research 结果

## Output

- `plan.md`
- 模板来源：[docs/templates/plan-template.md](../../docs/templates/plan-template.md)

## Procedure

1. 用架构和数据流描述“打算怎么做”，而不是重复 spec。
2. 列出真实触点，包括文件、模块、文档与外部输入。
3. 给出有因果关系的 `implementation_order`。
4. 写清风险、测试策略和 rollout / rollback 思路。
5. 显式标出当前不做的内容，避免范围悄悄膨胀。

## Completion Standard

- 其他执行者可以基于 `plan.md` 开始拆任务
- 已知风险和验证方式都有明确落点

## Guardrails

- 不跳过测试策略
- 不把“还没想清楚”伪装成“后面自然会处理”
- 不用大而全框架术语替代本环境现有术语

## Handoff

- `plan.md` 完成后默认交给 `method-forge-plan-review`
