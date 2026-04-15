# Spec / 规格

## Goals / 目标

- 让 autonomous run 以“用户当前顶层目标”为停止粒度，而不是以“单个微切片”作为默认停止粒度。
- Make autonomous runs stop at the granularity of the user's current top-level goal instead of defaulting to the granularity of a single micro-slice.

- 把“下一安全切片已知时保持 `running`”写成显式规则，减少执行歧义。
- Make “stay `running` when the next safe slice is already known” an explicit rule to reduce execution ambiguity.

## Non-Goals / 非目标

- 不重做 Codex 原生 heartbeat / automation 平台
- 不改变 loop guard 上限
- 不删除 `blocked` / `waiting-human` / `waiting-external` 这些停机状态

- Do not rebuild the native Codex heartbeat / automation platform
- Do not change the loop-guard budgets
- Do not remove the `blocked` / `waiting-human` / `waiting-external` stop states

## Functional Rules / 功能规则

- `completed` 只能表示顶层任务或当前变更包目标已经结束
- 若同一用户目标下下一安全切片已明确，不应因为某个微切片完成或通过 `verify` 就退出
- heartbeat prompt、resume rules、skill、消费方 AGENTS 必须对齐这一语义

- `completed` may only mean the top-level task or current change-package goal is finished
- If the next safe slice inside the same user goal is already known, the run should not exit just because one micro-slice finished or passed `verify`
- The heartbeat prompt, resume rules, skill, and consumer AGENTS must align on this semantic
