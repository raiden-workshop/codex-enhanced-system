# Spec

## Goal

- 为 `method-forge` 提供清晰的 orchestration 入口文档和 README 入口说明。

## User Value

- 新 worker 读完入口文档后，可以直接判断从哪里开始、复杂任务如何走、实现后如何收尾。

## In Scope

- 更新根 `README.md` 的标准流程入口说明
- 新增 `route-request`、`spec-flow`、`verify-and-memory` 的行为文档
- 保证方法规则文档与 orchestration 文档术语一致

## Out Of Scope

- 实现自动执行器
- 改造 memory system
- 改造 knowledge base
- 复制 Codex 原生 automations 或审批系统

## Constraints

- technical_constraints: 仅使用 Markdown 文档与现有目录结构落地。
- workflow_constraints: 会话内流程编排必须统一叫 `orchestrations`。
- policy_constraints: 不得重复实现 Codex 原生 multi-agent、worktree、git/PR、background automations。

## Acceptance Criteria

- `README.md` 明确指出从 `route-request` 开始，收尾进入 `verify-and-memory`
- 3 个 orchestration 文档都定义了目标、前置条件或输入、顺序和边界
- 任何文档都不把会话内流程重新叫成 `automations`
- 文档中明确写出 memory candidate 只能提出，不能直接写 memory

## Open Questions

- 无阻塞性未决问题；对高风险任务是否要求人工确认，先作为推荐规则写入，不做强制审批系统。
