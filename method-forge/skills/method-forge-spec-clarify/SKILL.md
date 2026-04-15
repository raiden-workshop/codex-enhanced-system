# method-forge-spec-clarify

## Purpose

把请求从“想做什么”压成稳定的 `spec.md`，让目标、边界和验收成为后续计划的真相源。

## Use When

- `intake.md` 判定 `need_spec=true`
- 任务存在边界不清、跨文件或中高风险因素时

## Inputs

- `intake.md`
- 用户目标
- 必要的研究材料

## Output

- `spec.md`
- 模板来源：[docs/templates/spec-template.md](../../docs/templates/spec-template.md)

## Procedure

1. 提炼唯一主目标，避免把多个目标混成一个大需求。
2. 写清 `user_value`，说明为什么值得做。
3. 划清 `in_scope` 与 `out_of_scope`。
4. 列出硬约束和验收标准。
5. 保留仍需确认的 `open_questions`，不要假装它们已经解决。

## Completion Standard

- `goal`、`scope`、`constraints`、`acceptance_criteria` 足够稳定
- 技术实现尚未过早展开

## Guardrails

- 不把 plan 级技术细节塞进 spec
- 不忽略旧规则与最新环境规则的冲突
- 如果发现冲突，以最新环境规则为准并在文档里写明修正

## Handoff

- `spec.md` 稳定后交给 `method-forge-plan-write`
- 如果 `open_questions` 仍然阻塞核心目标，先停下来补澄清
