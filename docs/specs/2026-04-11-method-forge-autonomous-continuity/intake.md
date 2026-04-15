# Intake / 需求摄取

## Request / 请求

- 用户指出：已经激活了自动流程，为什么还是频繁停下来，需要再次说“继续”才继续。
- The user pointed out that autonomous mode had already been activated, so it should not have kept stopping and waiting for another “continue”.

## Problem / 问题

- 当前规则强调 `completed` 后要停止，但没有足够明确地区分“顶层任务完成”和“单个微切片完成”。
- 这让执行者容易把 autonomous 误用成“每完成一刀就停”的半自动流程。

- The current rules correctly say to stop on `completed`, but they do not distinguish clearly enough between “the top-level task is done” and “one micro-slice is done.”
- That makes it too easy to use autonomous as a semi-manual flow that stops after every slice.

## Scope / 范围

- 明确 `completed` 的语义边界
- 明确“已知下一安全切片时要保持 running”
- 同步到 method-forge 文档、skill、模板和消费方 AGENTS

- Clarify the semantic boundary of `completed`
- Clarify that the run should stay `running` when the next safe slice is already known
- Sync the rule into method-forge docs, the skill, templates, and consumer AGENTS
