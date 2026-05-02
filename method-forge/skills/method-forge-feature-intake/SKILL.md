---
name: method-forge-feature-intake
description: Use when turning a raw request into intake.md and deciding whether to route into spec flow, direct execution, or research.
---

# method-forge-feature-intake

## Purpose

把原始请求压成一个可路由的 `intake.md`，明确下一步是直接实现、先 diagnosis、先 research，还是进入完整 spec 流。

## Use When

- 收到任何非闲聊、非纯问答请求时
- 需要判断任务复杂度、风险和文档流入口时

## Inputs

- 用户原始请求
- 当前 workspace 上下文
- 当前 `AGENTS.md`
- 必要的 memory / knowledge-base 索引

## Output

- `intake.md`
- 模板来源：[docs/templates/intake-template.md](../../docs/templates/intake-template.md)

## Procedure

1. 用一句话重述请求，避免把原始需求直接散落在会话里。
2. 判断 `task_type`、`risk_level`、`need_spec`、`need_research` 和 `need_memory_lookup`。
3. 产出 `suggested_path`，只能在 `direct-implement`、`diagnose-first`、`research-first`、`spec-flow` 中选择。
4. 当请求是 bug、失败、性能退化或不稳定行为，且当前没有可靠反馈环时，优先选择 `diagnose-first`。
5. 明确 `next_step`，让后续执行者不必重新判断流程入口。

## Completion Standard

- 已明确回答“现在应该做什么”
- 后续执行者可以基于 `intake.md` 直接继续，不需要再次做总分流

## Guardrails

- 不在 intake 阶段展开实现细节
- 不把 bug 报告直接当成可修复根因；缺少反馈环时先诊断
- 不直接写长期 memory
- 不把 research 结论当作 spec 替代品

## Handoff

- `suggested_path=direct-implement` 时，交给实现并在收尾进入 `verify-change`
- `suggested_path=diagnose-first` 时，交给 `method-forge-diagnose`，再根据根因回到实现或 spec-flow
- `suggested_path=research-first` 时，先补研究，再回到 `spec-clarify` 或实现
- `suggested_path=spec-flow` 时，交给 `method-forge-spec-clarify`
