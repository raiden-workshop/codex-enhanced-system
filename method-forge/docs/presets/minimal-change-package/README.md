# Minimal Change Package Preset

## Purpose

这是一个给消费方 workspace 使用的轻量 preset 入口。

它定义的是“如何组织一个变更包”，不是安装器，也不是新的 workflow 引擎。

## Recommended Tree

```text
docs/specs/<change-id>/
├── package-index.md
├── intake.md
├── spec.md
├── plan.md
├── plan-review.md
├── tasks.md
├── verify.md
├── code-review.md
├── memory-candidate.md
├── workflow-health-report.md
└── runtime/
    ├── run-state.md
    └── reports/
```

## Required Files

- `package-index.md`
- `intake.md`
- `verify.md`

复杂任务再补：

- `spec.md`
- `plan.md`
- `plan-review.md`
- `tasks.md`

## Optional Files

- `code-review.md`
- `memory-candidate.md`
- `workflow-health-report.md`
- `runtime/run-state.md`

## Use These Templates

- [consumer-agents-rules-template.md](../../templates/consumer-agents-rules-template.md)
- [package-index-template.md](../../templates/package-index-template.md)
- [intake-template.md](../../templates/intake-template.md)
- [spec-template.md](../../templates/spec-template.md)
- [plan-template.md](../../templates/plan-template.md)
- [plan-review-template.md](../../templates/plan-review-template.md)
- [tasks-template.md](../../templates/tasks-template.md)
- [verify-template.md](../../templates/verify-template.md)
- [code-review-template.md](../../templates/code-review-template.md)
- [memory-candidate-template.md](../../templates/memory-candidate-template.md)
- [workflow-health-report-template.md](../../templates/workflow-health-report-template.md)
- [run-state-template.md](../../templates/run-state-template.md)
- [autonomous-cycle-report-template.md](../../templates/autonomous-cycle-report-template.md)
- [autonomous-heartbeat-prompt-template.md](../../templates/autonomous-heartbeat-prompt-template.md)
- [adoption-checklist-template.md](../../templates/adoption-checklist-template.md)

## Notes

- 若消费方希望一句话触发整条流程，可以直接使用 [method-forge-execute](../../../skills/method-forge-execute/SKILL.md) 的自然语言入口。
- 若消费方希望“开始落地代码”“开始实现”“继续写代码”等实现意图默认自动续跑到本轮结束，应同时接入 [method-forge-autonomous-execution](../../../skills/method-forge-autonomous-execution/SKILL.md) 和 heartbeat automation prompt。
- 若消费方想手动显式启动 autonomous，也仍可直接使用 [method-forge-autonomous-execution](../../../skills/method-forge-autonomous-execution/SKILL.md)。
- 消费方可以先把 [consumer-agents-rules-template.md](../../templates/consumer-agents-rules-template.md) 贴进自己的 `AGENTS.md` 再细化。
- `package-index.md` 是导航页，不是第二份 spec。
- 若消费方只做轻任务，不必强制补齐所有文件。
- 仍然遵守 `method-forge` 的边界：不重做 Codex 原生 multi-agent、git/PR、automations、sandbox。
