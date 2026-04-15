# v1 Acceptance Report

## 1. 结论

`method-forge v1` 已完成最小可用交付。

本次交付严格保持在 Codex 兼容的方法层：

- 已建立目录结构
- 已落地 6 个模板
- 已落地 6 个核心 skill
- 已落地 3 个 orchestration
- 已补齐 workflow、skill contracts、orchestration rules、Codex native boundaries
- 已提供 1 组从 intake 到 verify 的示例闭环文档

## 2. 交付物

### 根文档

- `<repo-root>/method-forge/README.md`
- `<repo-root>/method-forge/AGENTS.md`

### 方法文档

- `<repo-root>/method-forge/docs/method/workflow.md`
- `<repo-root>/method-forge/docs/method/skill-contracts.md`
- `<repo-root>/method-forge/docs/method/orchestration-rules.md`
- `<repo-root>/method-forge/docs/method/codex-native-boundaries.md`
- `<repo-root>/method-forge/docs/method/v1-acceptance-report.md`

### 模板

- `<repo-root>/method-forge/docs/templates/intake-template.md`
- `<repo-root>/method-forge/docs/templates/spec-template.md`
- `<repo-root>/method-forge/docs/templates/plan-template.md`
- `<repo-root>/method-forge/docs/templates/plan-review-template.md`
- `<repo-root>/method-forge/docs/templates/tasks-template.md`
- `<repo-root>/method-forge/docs/templates/verify-template.md`

### Skills

- `<repo-root>/method-forge/skills/method-forge-feature-intake/SKILL.md`
- `<repo-root>/method-forge/skills/method-forge-spec-clarify/SKILL.md`
- `<repo-root>/method-forge/skills/method-forge-plan-write/SKILL.md`
- `<repo-root>/method-forge/skills/method-forge-plan-review/SKILL.md`
- `<repo-root>/method-forge/skills/method-forge-task-breakdown/SKILL.md`
- `<repo-root>/method-forge/skills/method-forge-verify-change/SKILL.md`

### Orchestrations

- `<repo-root>/method-forge/orchestrations/route-request/README.md`
- `<repo-root>/method-forge/orchestrations/spec-flow/README.md`
- `<repo-root>/method-forge/orchestrations/verify-and-memory/README.md`

### 示例闭环

- `<repo-root>/method-forge/docs/method/examples/sample-change/intake.md`
- `<repo-root>/method-forge/docs/method/examples/sample-change/spec.md`
- `<repo-root>/method-forge/docs/method/examples/sample-change/plan.md`
- `<repo-root>/method-forge/docs/method/examples/sample-change/plan-review.md`
- `<repo-root>/method-forge/docs/method/examples/sample-change/tasks.md`
- `<repo-root>/method-forge/docs/method/examples/sample-change/verify.md`

## 3. 边界判定

### 交给 Codex 原生的能力

- multi-agent 调度
- worktree 隔离
- diff review 和变更面板
- git / commit / PR 基础集成
- background automations
- sandbox / approvals
- skill loading

### 由 `method-forge` 实现的能力

- request intake 规则
- `spec -> plan -> tasks -> verify` 文档流
- `plan-review` 与 `verify-change` 质量门
- 会话内 `orchestrations`
- memory candidate 判断
- knowledge-base 输入边界

## 4. 与最新规则的冲突修正

已显式修正旧表述中的术语冲突：

- 会话内流程编排统一使用 `orchestrations`
- `automations` 仅指 Codex App 原生后台任务

这条修正已同时写入：

- `AGENTS.md`
- `workflow.md`
- `orchestration-rules.md`
- `codex-native-boundaries.md`
- 3 个 orchestration README

## 5. 示例闭环验证

示例任务选择的是一个真实且足够小的文档型复杂任务：

- 为 `method-forge` 新增 orchestration 入口文档，并把根 `README.md` 补成可导航入口

闭环产物位于：

- `<repo-root>/method-forge/docs/method/examples/sample-change/`

验证通过标准：

- 已存在完整的 `intake/spec/plan/plan-review/tasks/verify`
- `plan-review.md` 为 `approved`
- `verify.md` 明确记录行为验证、测试验证、风险判断、文档同步和 memory candidate
- 示例中的 memory candidate 只提出候选，不直接写 memory

本次实际检查包括：

- 通过 `rg --files <repo-root>/method-forge` 确认必需文件全部存在
- 通过关键字检索确认 `need_spec`、`approval_status`、`memory_candidate` 和 `orchestrations` 等关键字段已落到模板、skills、orchestrations 与示例文档
- 人工顺读根 `README.md` 与 3 个 orchestration README，确认入口、复杂流和收尾流连贯

## 6. 当前风险与后续建议

- `v1` 仍以文档和 skill 契约为主，没有独立执行引擎；这是刻意保持轻量的结果，不是遗漏。
- 复杂任务的人类确认点目前只写成推荐规则，后续若要统一治理，可在 `v1.5` 增补失败回退和确认协议。
- `code-review` 与 `memory-promote` 还未纳入 `v1`，建议在后续版本补齐。
- 消费方仓库的产物目录约定目前保持推荐而非强制，后续若跨项目复用增多，可收敛成 preset。
