---
name: method-forge-execute
description: Use when the user says phrases like "按method-forge方式执行", "按 method-forge 执行", "use method-forge", or wants one worker to take a raw requirement or rough design docs, normalize them into intake/spec/plan, fill missing quality gates, decide light vs complex flow, and continue through tasks, implementation, verify, optional code-review, and memory-candidate without switching workers.
---

# method-forge-execute

## Purpose

这是 `method-forge` 的单入口 skill。

它让用户只用一句自然语言就能进入整条方法流，而不需要先手工准备标准化 md，也不需要在不同 worker 间切换。

## Use When

- 用户说“按method-forge方式执行”
- 用户给出项目需求，希望按 `method-forge` 端到端推进
- 用户已经有粗粒度设计文档，但希望自动补齐 `intake/spec/plan/tasks/verify`
- 用户希望在同一个 worker 里完成归一化、补质量门、实现和 verify

## Inputs

- 用户原始需求
- 已有设计文档、方案草稿或需求说明
- 当前 workspace / repo 上下文

## Default Assumptions

- 已有设计文档只是输入材料，不天然等于标准化的 `spec.md` 或 `plan.md`
- 若代码仓库上下文足够，就在同一个 worker 里继续实现与 verify
- 若当前只具备需求信息而没有可实现上下文，就先停在 `intake/spec/plan`
- 若处于 autonomous 模式，本 skill 可被默认作为内层执行引擎调用，不需要用户每轮重复指定

## Procedure

1. 读取用户需求与已有设计材料，先建立或更新当前变更包。
2. 默认在当前 workspace 使用 `docs/specs/<date>-<slug>/` 作为变更包目录，并先创建或更新 `package-index.md`。
3. 按 [method-forge-feature-intake](../method-forge-feature-intake/SKILL.md) 产出 `intake.md`，判断轻任务还是复杂任务。
4. 若 `suggested_path=diagnose-first`，先按 [method-forge-diagnose](../method-forge-diagnose/SKILL.md) 建立反馈环和根因判断，再决定直接实现或回到 spec-flow。
5. 若 `need_spec=true`，按 [spec-flow](../../orchestrations/spec-flow/README.md) 归一化已有设计材料，补齐 `spec.md`、`plan.md`、`plan-review.md`、`tasks.md`。
6. 若用户已有设计文档，优先映射与补缺，不机械复制原文。
7. 若实现上下文足够，直接在同一 worker 里执行任务。
8. 高风险改动按需追加 [method-forge-code-review](../method-forge-code-review/SKILL.md)。
9. 完成后统一走 [verify-and-memory](../../orchestrations/verify-and-memory/README.md)，产出 `verify.md`。
10. 若 `verify.md` 判定存在稳定候选，再按 [method-forge-memory-promote](../method-forge-memory-promote/SKILL.md) 产出 `memory-candidate.md`。

## Outputs

最少输出：

- `package-index.md`
- `intake.md`

复杂任务常见输出：

- `spec.md`
- `plan.md`
- `plan-review.md`
- `tasks.md`

实现后输出：

- `verify.md`
- `code-review.md`（可选）
- `memory-candidate.md`（可选）

## Stop Conditions

- 用户要改代码，但当前没有足够 workspace / repo 上下文
- 需求存在高风险歧义，继续假设会造成明显返工
- 外部依赖或权限前提缺失，导致无法安全实现

## Guardrails

- 不要求用户先手工写完标准化 md 再开始
- 不要求用户切换到别的 worker 才能继续
- 不把粗稿设计文档直接当作最终真相源
- 不在缺少反馈环的 bug / regression 请求上跳过 diagnosis
- 不直接写长期 memory
- 不重复实现 Codex 原生 multi-agent、git/PR、automations、sandbox

## Quick Invocation

用户可以直接这样说：

- `按method-forge方式执行这个需求：...`
- `按 method-forge 执行，需求如下：...`
- `这里有一份设计草稿，按method-forge方式执行并补齐文档与实现`
