# Codex Native Boundaries

## 1. 目的

`method-forge` 只补齐 Codex App 没有替项目定义好的“方法层”。

如果不先划清边界，很容易把原生能力又包成第二套平台，结果是规则变多、入口变重、维护成本变高。

## 2. Codex App 原生负责

以下能力保持交给 Codex App 或当前环境原生机制：

| 能力 | 归属 | `method-forge` 的态度 |
| --- | --- | --- |
| multi-agent 调度 | Codex 原生 | 直接复用，不再封装第二套团队系统 |
| worktree 隔离 | Codex 原生 | 直接复用，不重做工作区管理层 |
| diff review / 变更面板 | Codex 原生 | 直接复用，不另做审阅 UI |
| git / commit / PR 基础集成 | Codex 原生 | 直接复用，只在方法文档里说明何时需要 review |
| background automations | Codex 原生 | 不在本项目中复制后台调度器 |
| sandbox / approvals / trust | Codex 原生 | 不重做权限系统 |
| skill loading | Codex 原生 | 只编写 `SKILL.md`，不实现加载器 |
| heartbeat / background automation 调度 | Codex 原生 | 可提供 prompt 与状态规则，但不重做监听器 |

## 3. `method-forge` 自定义负责

以下能力属于 `method-forge v1`：

| 能力 | 说明 |
| --- | --- |
| Intake 规则 | 把原始请求标准化并路由 |
| `spec -> plan -> tasks -> verify` 文档流 | 为复杂任务提供真相源 |
| `plan-review` 与 `verify` 质量门 | 保持执行纪律与验收边界 |
| `orchestrations` | 只做会话内流程编排 |
| memory candidate 判断 | 只提出候选，不直接写 memory |
| knowledge-base 接入口 | 把 research 结果接入 spec/plan，但不替代它们 |
| autonomous run-state / resume / loop guard | 为原生 automation 提供方法层状态与恢复规则 |

## 4. 明确不做的事

`v1` 明确不做：

- 改造全局 memory system
- 改造 knowledge base 本体
- 引入完整外部框架安装器
- 把外部 GitHub 项目目录原样搬进来
- 重做原生多 agent、worktree、background automations 或 diff review

## 5. 命名修正

参考资料和旧环境中可能出现过“`skills + automations`”的表述。

按当前最新规则，必须改成：

- `skills`：能力单元
- `orchestrations`：会话内流程编排
- `automations`：Codex App 原生后台任务

这条修正优先于旧说法，是 `method-forge` 当前实现的硬边界。

补充：

- autonomous 模式里，真正的监听者仍然是 Codex 原生 automation
- `method-forge` 只负责默认执行引擎、run-state、resume 和 loop guard

## 6. 和 memory / knowledge base 的边界

- memory system 回答“应该长期记住什么”
- knowledge base 回答“知道什么”
- `method-forge` 回答“一个请求应该如何稳定地走到交付”

三者互补，但不能混层。
