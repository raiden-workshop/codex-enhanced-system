# Skill Contracts

## 1. 通用契约

所有 `method-forge-*` skills 共用以下规则：

- 输入尽量来自已存在的请求、仓库上下文和上一步文档
- 输出以单一主文档为准，不把真相源散落在聊天文本里
- 默认使用 [docs/templates/](../templates) 中的模板
- 不直接写长期 memory
- 不改造 knowledge base 本体
- 不包装 Codex 原生工程能力
- 不实现 Codex 原生 lifecycle hooks 的替代 runner

实现 skills 时保持规则简单、稳定、可验证，只补缺口，不扩成新的复杂约定。

## 2. 核心技能总表

| Skill | 作用 | 主要输入 | 主要输出 | 下一步门 |
| --- | --- | --- | --- | --- |
| `method-forge-feature-intake` | 标准化请求并分流 | 原始请求、workspace 上下文 | `intake.md` | 明确直接实现、research 或 spec-flow |
| `method-forge-spec-clarify` | 固化目标、范围与验收 | `intake.md`、研究材料 | `spec.md` | 进入 `plan-write` |
| `method-forge-plan-write` | 生成技术实现方案 | `spec.md`、仓库上下文 | `plan.md` | 进入 `plan-review` |
| `method-forge-plan-review` | 计划质量门 | `spec.md`、`plan.md` | `plan-review.md` | `approved` 才能拆任务 |
| `method-forge-task-breakdown` | 形成可执行任务清单 | `plan.md`、`plan-review.md` | `tasks.md` | 进入实现 |
| `method-forge-verify-change` | 验证交付是否完成 | 变更结果、前序文档、测试结果 | `verify.md` | 决定是否可交付及是否有 memory candidate |

## 2.0 入口技能

| Skill | 作用 | 主要输入 | 主要输出 | 下一步门 |
| --- | --- | --- | --- | --- |
| `method-forge-execute` | 让用户用一句自然语言触发整条方法流 | 原始需求、粗稿设计文档、当前 workspace | `package-index.md` + 归一化后的 workflow 文档包 | 自动决定轻任务流或复杂任务流，并在可行时继续实现与 verify |

## 2.0.5 autonomous 技能

| Skill | 作用 | 主要输入 | 主要输出 | 下一步门 |
| --- | --- | --- | --- | --- |
| `method-forge-autonomous-execution` | 让任务在 heartbeat 模式下自动续跑并可恢复 | 原始需求、变更包、run-state、当前 workspace | `run-state.md` + cycle reports + heartbeat prompt 草案 | 默认在每轮周期自动调用 `method-forge-execute`，直到完成或安全停机 |

## 2.1 `v1.5` 可选增强技能

| Skill | 作用 | 主要输入 | 主要输出 | 下一步门 |
| --- | --- | --- | --- | --- |
| `method-forge-code-review` | 对实现做正确性与回归风险审查 | 改动结果、前序文档、测试结果 | `code-review.md` | 决定是否先修复再 verify |
| `method-forge-memory-promote` | 整理 memory 候选 | `verify.md`、可选 review 结论 | `memory-candidate.md` | 交给既有 memory 流程人工处理 |

## 3. 单个 Skill 的强约束

### 3.1 `method-forge-feature-intake`

- 必须产出任务分类、风险等级和下一步建议
- 必须回答是否需要 `spec`、research 和 memory lookup
- 不展开实现细节

### 3.2 `method-forge-spec-clarify`

- 必须把“做什么”和“为什么”写清楚
- 必须明确 `in_scope` 与 `out_of_scope`
- 不在这一阶段堆技术方案

### 3.3 `method-forge-plan-write`

- 必须覆盖架构、数据流、触点、顺序、风险、测试与 rollout
- 必须说明为什么这个顺序是合理的
- 不跳过已知风险

### 3.4 `method-forge-plan-review`

- 发现项优先，摘要次之
- 必须判断是否有缺失测试、过度设计、顺序问题和歧义
- 输出必须给出 `approved` 或 `needs-revision`

### 3.5 `method-forge-task-breakdown`

- 每个任务至少包含：`id`、`goal`、`files`、`depends_on`、`verification`、`done_definition`
- 任务粒度以“能独立执行和回滚”为准
- 当 `plan-review` 未批准时不得继续

### 3.6 `method-forge-verify-change`

- 必须同时验证行为、测试、回归风险与文档同步
- 如果没有完整 spec 流，至少要对照 `intake.md` 和实际改动做验证
- 可以提出 memory candidate，但不能直接写 memory

### 3.6.5 `method-forge-execute`

- 必须先把已有设计材料归一化，再决定是否继续实现
- 默认不要求用户先手工写标准化 md
- 默认不把用户赶去别的 worker；能在当前 worker 完成的就继续完成

### 3.6.6 `method-forge-autonomous-execution`

- 必须使用 Codex 原生 automation 作为监听器，而不是重做第二套调度器
- 当用户表达“开始落地代码”“开始实现”“开始写代码”“继续写代码”等实现意图时默认启用；显式要求 automation / autonomous / heartbeat 续跑或恢复既有 autonomous run 时也启用
- 必须把 `method-forge-execute` 设为默认内层执行引擎
- 必须维护 `run-state.md` 并执行 loop guard
- 不得把 lifecycle hooks 当作 heartbeat 的替代品；hooks 只适合即时事件前后处理

### 3.7 `method-forge-code-review`

- findings 必须优先于摘要
- 必须区分阻塞问题、建议项和残余风险
- 不复制 Codex 原生 diff review，只产出方法层审查结论

### 3.8 `method-forge-memory-promote`

- 必须能追溯回 `verify.md`
- 必须只保留稳定、可复用、可压缩的最小结论
- 输出始终保持 `candidate-only`，不得直接写 memory

## 4. 与实现层的交接

`method-forge` 不把“implement”做成独立 skill。

`tasks.md` 交给主 agent 或消费方执行，执行后再由 `method-forge-verify-change` 负责验收闭环。

当任务风险较高时，推荐在实现后接入：

- `method-forge-code-review`
- `method-forge-verify-change`
- `method-forge-memory-promote`
