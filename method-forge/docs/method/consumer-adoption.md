# Consumer Adoption

## 1. 目的

这份文档说明其他 workspace 如何以最小成本接入 `method-forge`，而不需要把当前 workspace 整体复制过去。

目标是给消费方一套轻量、可 diff、可交接的落地方式：

- 推荐目录
- 最小接入步骤
- 变更包索引
- 落地检查清单

## 2. 推荐接入方式

消费方 workspace 不需要搬运整个 `method-forge/` 目录。

推荐只做两层接入：

1. 在自己的 workspace 中采用 `docs/specs/<change-id>/` 产物包约定。
2. 参考 `method-forge` 的方法文档、模板和 skills 规则来驱动实际执行。

## 3. 推荐目录

复杂变更推荐使用：

```text
<consumer-workspace>/
├── AGENTS.md
└── docs/
    └── specs/
        └── <change-id>/
            ├── package-index.md
            ├── intake.md
            ├── spec.md
            ├── plan.md
            ├── plan-review.md
            ├── tasks.md
            ├── verify.md
            ├── code-review.md           # optional
            ├── memory-candidate.md      # optional
            ├── workflow-health-report.md # optional
            └── runtime/
                ├── run-state.md         # optional
                └── reports/             # optional
```

轻任务最少保留：

- `package-index.md`
- `intake.md`
- `verify.md`

## 4. 最小接入步骤

1. 在消费方 `AGENTS.md` 写入硬规则，只保留必须遵守的入口、质量门和边界。
2. 约定复杂任务落在 `docs/specs/<change-id>/`。
3. 使用 `package-index.md` 作为单个变更包导航页。
4. 复杂任务按 `intake -> spec -> plan -> plan-review -> tasks -> verify` 走。
5. 高风险任务按需追加 `code-review` 和 `memory-candidate`。
6. 定期用 `workflow-health-report.md` 做人工健康检查。
7. 若采用默认行为，则在用户表达“开始落地代码”“开始实现”“继续写代码”等实现意图时启用 `runtime/run-state.md` 和 Codex App 原生 heartbeat automation。

若你希望支持默认 implementation-intent -> autonomous 触发，或恢复既有 autonomous run，还需要：

- 让入口 skill 在所有 worker 中可见
- 在消费方 `AGENTS.md` 中写入触发短语规则

如果希望尽量少手工操作，可以直接对 Codex 说：

- `按method-forge方式执行这个需求：...`

在这种用法下，入口 skill 会把你的自然语言需求或粗稿设计文档自动归一化为标准变更包。

## 5. 必需与可选产物

### 必需

- `package-index.md`
- `intake.md`
- `verify.md`

### 复杂任务必需

- `spec.md`
- `plan.md`
- `plan-review.md`
- `tasks.md`

### 可选增强

- `code-review.md`
- `memory-candidate.md`
- `workflow-health-report.md`
- `runtime/run-state.md`
- `runtime/reports/<cycle>.md`

## 6. 落地规则

- `package-index.md` 只做导航和状态，不重复写各阶段全文
- 每个产物文件只承载一个主真相源
- 失败时回到原真相源修订，不另开平行版本
- `memory-candidate.md` 只整理候选，不直接写 memory
- 会话内流程继续统一叫 `orchestrations`
- autonomous 模式下，heartbeat 应默认使用 `method-forge-execute`
- 普通实现意图默认可以进入后台 automation；若消费方不希望自动，必须显式声明降级短语

## 7. 入口文件

当前已提供以下配套：

- 接入说明：[docs/method/consumer-adoption.md](consumer-adoption.md)
- autonomous 扩展说明：[docs/method/autonomous-execution.md](autonomous-execution.md)
- 自动激活规则：[docs/method/activation-rules.md](activation-rules.md)
- autonomous 入口 skill：[skills/method-forge-autonomous-execution/SKILL.md](../../skills/method-forge-autonomous-execution/SKILL.md)
- 单入口 skill：[skills/method-forge-execute/SKILL.md](../../skills/method-forge-execute/SKILL.md)
- preset 入口：[docs/presets/minimal-change-package/README.md](../presets/minimal-change-package/README.md)
- `AGENTS.md` 硬规则草案：[docs/templates/consumer-agents-rules-template.md](../templates/consumer-agents-rules-template.md)
- 变更包索引模板：[docs/templates/package-index-template.md](../templates/package-index-template.md)
- 落地检查清单模板：[docs/templates/adoption-checklist-template.md](../templates/adoption-checklist-template.md)

## 8. 当前边界

这仍然是轻量 preset，不是完整安装器。

它不做：

- 自动创建消费方目录
- 自动复制模板
- 自动注入 `AGENTS.md`
- 自动接管 Codex 原生能力
