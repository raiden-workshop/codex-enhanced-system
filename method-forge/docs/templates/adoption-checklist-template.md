# Adoption Checklist

Keep the adopted workflow simple, explicit, and tightly scoped: think before adding rules, change only what is needed, and verify each required artifact.

## Workspace Setup

- [ ] `AGENTS.md` 已写入入口、质量门和边界硬规则
- [ ] 已约定复杂任务目录为 `docs/specs/<change-id>/`
- [ ] 已确认会话内流程统一叫 `orchestrations`

## Package Setup

- [ ] 已创建 `package-index.md`
- [ ] 已为本次任务创建 `intake.md`
- [ ] 已根据复杂度决定是否需要 `spec.md`
- [ ] 已确认 `verify.md` 是必需收尾产物

## Quality Gates

- [ ] 已启用 `plan-review` 作为复杂任务默认质量门
- [ ] 已明确何时需要 `code-review`
- [ ] 已明确何时允许提出 `memory-candidate`

## Boundaries

- [ ] 不直接写长期 memory
- [ ] 不重做 Codex 原生 multi-agent、git/PR、automations、lifecycle hooks、sandbox
- [ ] 不把 research 或 knowledge-base 页面当成 `spec.md` / `plan.md` 替代品

## Maintenance

- [ ] 已采用模板 lint 规则
- [ ] 已约定失败后回到原真相源修订
- [ ] 已约定何时做 `workflow-health-report`

## Autonomous Mode Optional

- [ ] 已约定 autonomous 模式的 `runtime/run-state.md` 路径
- [ ] 已采用 loop guard 规则
- [ ] 已明确 heartbeat automation 默认使用 `method-forge-execute`
- [ ] 已明确 lifecycle hooks 只用于即时事件，不替代 heartbeat 续跑
