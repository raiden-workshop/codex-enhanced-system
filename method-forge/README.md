# method-forge

`method-forge` 是一套面向 Codex App 的 spec-driven workflow 方法层子系统。

它负责把原始请求稳定地推进为可落盘、可评审、可交接的交付流，核心产物是：

- `intake -> spec -> plan -> plan-review -> tasks -> verify`
- 原子 `skills`
- 会话内 `orchestrations`
- 明确的质量门与 memory candidate 判断

它不重复实现 Codex App 已经原生提供的工程能力。

仓库级原生优先边界以根目录 [README.md](../README.md) 里的 `Native-first compatibility map` 为准；本文档只细化 `method-forge` 自己的方法层职责。

使用 `method-forge` 时，同样保持这套通用原则：先想清楚再写、简单优先、只做必要改动、先定义成功标准再验证。

## 负责范围

- 请求 intake 与任务分流
- 复杂任务的 `spec -> plan -> tasks` 文档流
- `plan-review` 与 `verify` 质量门
- 研究结果、知识库、memory candidate 的接入口边界
- 面向新 worker 的 Markdown 方法文档、模板与 skill 契约

## 不负责范围

- multi-agent 调度
- worktree 隔离
- diff review 面板
- git / commit / PR 基础集成
- background automations
- lifecycle hooks / hook runner
- plugins / app integrations / MCP 分发
- Computer Use
- built-in image generation
- native memories
- sandbox / approvals / trust 配置
- skill 加载机制
- memory system 本体改造
- knowledge base 本体改造

## 目录

```text
method-forge/
├── AGENTS.md
├── README.md
├── docs/
│   ├── method/
│   └── templates/
├── skills/
└── orchestrations/
```

## 标准流程

轻任务：

```text
route-request
-> feature-intake
-> implement
-> verify-and-memory
```

复杂任务：

```text
route-request
-> feature-intake
-> spec-flow
-> spec-clarify
-> plan-write
-> plan-review
-> task-breakdown
-> implement
-> verify-and-memory
```

## 快速使用

1. 从 [orchestrations/route-request/README.md](orchestrations/route-request/README.md) 开始，对请求做 intake 和分流。
2. 当 `need_spec=true` 时，进入 [orchestrations/spec-flow/README.md](orchestrations/spec-flow/README.md)。
3. 以 [docs/templates/](docs/templates) 中的模板产出中间文档。
4. 实现完成后，始终走 [orchestrations/verify-and-memory/README.md](orchestrations/verify-and-memory/README.md)。

如果你不想手动分步骤，可以直接触发入口 skill：

- [method-forge-execute/SKILL.md](skills/method-forge-execute/SKILL.md)
- [method-forge-autonomous-execution/SKILL.md](skills/method-forge-autonomous-execution/SKILL.md)

一句话用法：

- `按method-forge方式执行这个需求：...`
- `这里有一份设计草稿，按method-forge方式执行并补齐缺的文档、实现和 verify`
- `开始落地代码，让 method-forge 自动跑到本轮任务结束`
- `启动 autonomous mode，用 method-forge 自动跑到本轮任务结束`

## 核心文档

- 流程说明：[docs/method/workflow.md](docs/method/workflow.md)
- Skill 契约：[docs/method/skill-contracts.md](docs/method/skill-contracts.md)
- Orchestration 规则：[docs/method/orchestration-rules.md](docs/method/orchestration-rules.md)
- 仓库级兼容图：[../README.md#native-first-compatibility-map](../README.md#native-first-compatibility-map)
- Codex 原生边界：[docs/method/codex-native-boundaries.md](docs/method/codex-native-boundaries.md)
- 单入口执行 skill：[skills/method-forge-execute/SKILL.md](skills/method-forge-execute/SKILL.md)
- autonomous 执行扩展：[docs/method/autonomous-execution.md](docs/method/autonomous-execution.md)
- 自动激活规则：[docs/method/activation-rules.md](docs/method/activation-rules.md)
- autonomous 入口 skill：[skills/method-forge-autonomous-execution/SKILL.md](skills/method-forge-autonomous-execution/SKILL.md)
- 恢复规则：[docs/method/resume-rules.md](docs/method/resume-rules.md)
- 防死循环规则：[docs/method/loop-guard-rules.md](docs/method/loop-guard-rules.md)
- 运行态模板：[docs/templates/run-state-template.md](docs/templates/run-state-template.md)
- heartbeat prompt 模板：[docs/templates/autonomous-heartbeat-prompt-template.md](docs/templates/autonomous-heartbeat-prompt-template.md)
- `v1` 验收报告：[docs/method/v1-acceptance-report.md](docs/method/v1-acceptance-report.md)
- `v1.5` 补强报告：[docs/method/v1.5-hardening-report.md](docs/method/v1.5-hardening-report.md)
- 失败回退规则：[docs/method/failure-rework-rules.md](docs/method/failure-rework-rules.md)
- 模板 lint 规则：[docs/method/template-lint-rules.md](docs/method/template-lint-rules.md)
- 流程健康检查：[docs/method/workflow-health-check.md](docs/method/workflow-health-check.md)
- 消费方接入说明：[docs/method/consumer-adoption.md](docs/method/consumer-adoption.md)
- 消费方 `AGENTS` 草案：[docs/templates/consumer-agents-rules-template.md](docs/templates/consumer-agents-rules-template.md)
- 健康检查模板：[docs/templates/workflow-health-report-template.md](docs/templates/workflow-health-report-template.md)
- 健康检查样例：[docs/method/examples/health-check/workflow-health-report.md](docs/method/examples/health-check/workflow-health-report.md)
- 轻量 preset 入口：[docs/presets/minimal-change-package/README.md](docs/presets/minimal-change-package/README.md)

## 当前版本

`v1` 目标是跑通最小可用 workflow：

- 6 个模板
- 6 个核心 skill
- 3 个 orchestration
- 1 套边界清晰、可交接的说明文档

完整的 review 生态、自动 memory 晋升流程和跨 workspace preset 复用留到后续版本处理。

当前已补上的 `v1.5` 轻增强包括：

- 可选 `method-forge-code-review`
- 可选 `method-forge-memory-promote`
- failure / rework 规则
- 模板 lint 规则
- workflow health check
- workflow health report 模板与样例

当前也已补上 autonomous-execution 扩展：

- 原生 heartbeat automation 监听模型
- `run-state.md` 与 cycle report
- resume / loop guard 规则
- 默认自动调用 `method-forge-execute`
- lifecycle hooks 仍归 Codex 原生；`method-forge` 只说明何时适合挂接，不自动安装 hook 配置

如果你希望在每个 worker 里支持“开始落地代码 / 开始实现 / 继续写代码”等实现意图默认进入 autonomous mode，或恢复既有 autonomous run，还需要：

- 让入口 skill 全局可见
- 采用 [activation-rules.md](docs/method/activation-rules.md) 中的触发规则

当前也已经补上一个消费方可直接复用的轻量落地包：

- `docs/specs/<change-id>/` 目录约定
- `AGENTS.md` 硬规则草案
- `package-index.md` 模板
- adoption checklist 模板
- minimal change package preset 入口
