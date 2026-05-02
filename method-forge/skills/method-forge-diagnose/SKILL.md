---
name: method-forge-diagnose
description: Use when a user reports a bug, failing behavior, flaky behavior, performance regression, or unclear failure and the next safest step is to build a feedback loop before fixing.
---

# method-forge-diagnose

## Purpose

把 bug / failure / regression 类请求先压成可复现、可验证的诊断链，避免在没有反馈环的情况下猜测式修复。

## Use When

- 用户报告 bug、失败、报错、行为不一致或性能退化
- `intake.md` 判断 `suggested_path=diagnose-first`
- 修复前缺少可靠复现路径
- 高风险问题需要先区分假设，再决定正确修复层

## Inputs

- 用户描述的失败症状
- 当前 workspace / repo 上下文
- `intake.md`
- 相关日志、报错、测试输出或复现材料

## Output

- `diagnosis.md`
- 模板来源：[docs/templates/diagnosis-template.md](../../docs/templates/diagnosis-template.md)

## Procedure

1. 建立反馈环：优先使用最窄测试、CLI、HTTP 请求、fixture、browser script 或可重复命令。
2. 复现症状：确认反馈环命中用户描述的问题，而不是附近的另一个问题。
3. 列出 3-5 个可证伪假设，并写明每个假设的预测。
4. 只对排名最高且最便宜的假设做定向观察；临时插桩必须带唯一前缀。
5. 归纳根因和正确修复层。
6. 如果已经找到正确测试缝隙，把复现转成回归测试建议。
7. 清理临时插桩，或者在 `diagnosis.md` 中明确未清理原因和位置。

## Completion Standard

- 有可信反馈环，或明确说明为什么当前无法建立反馈环
- 症状、假设、证据、根因和下一步修复层清楚
- 后续执行者可以基于 `diagnosis.md` 继续实现或回到 spec/plan

## Guardrails

- 没有反馈环时，不进入猜测式修复
- 不把“看起来像”当根因
- 不把诊断日志长期留在代码里
- 不直接部署、不直接安装外部工具、不接管 Codex 原生能力
- 输出较长时遵循 [output-budget-policy.md](../../docs/method/output-budget-policy.md)

## Handoff

- 根因明确且风险低：交给实现路径，再运行 `method-forge-verify-change`
- 需要设计调整：回到 `method-forge-spec-clarify` 或 `method-forge-plan-write`
- 无法复现：停在 `blocked`，列出需要用户补充的证据

