# GitHub AI Workflow Adaptation Research

Date: 2026-05-02

## Goal

将外部 GitHub 项目的可复用方法沉淀为 `codex-enhanced-system` 的补足方案，而不是安装、部署或替换现有系统。

本方案严格遵循：

- Codex App 原生能力优先。
- 不覆盖现有 `method-forge` 流程。
- 不引入外部平台作为运行时依赖。
- 不启用全局 shell hook、daemon、代理或后台 runner。
- 只吸收方法、检查项、模板和可选 wrapper 设计。

## Scope

纳入研究：

- `rtk-ai/rtk`
- `coleam00/Archon`
- `mattpocock/skills`
- `forrestchang/andrej-karpathy-skills`
- `luongnv89/claude-howto`

明确跳过：

- `hugohe3/ppt-master`
- 其它 PPT 生成相关内容
- `microsoft/markitdown`

## Native-First Boundary

任何改造都必须先检查 Codex App 是否已有对应能力。

保持 Codex 原生负责：

- subagents / multi-agent
- worktree isolation
- diff review
- git / commit / PR flow
- heartbeat / background automations
- lifecycle hooks
- plugin / MCP / app integrations
- skill loading
- sandbox / approvals
- native memories

`codex-enhanced-system` 只补足：

- 方法层流程和质量门
- `spec -> plan -> tasks -> verify` 产物约束
- 输出预算和证据保留策略
- 外部方法的本地化 preset
- memory candidate 判断

## Project Findings

### rtk-ai/rtk

可吸收价值：

- 对命令输出做压缩，减少上下文污染。
- 区分测试、构建、git、lint 等输出类型。
- 保留失败优先、摘要优先、原始输出可追溯的思路。

不直接采用：

- 不执行 `rtk init --global`。
- 不安装 Codex hook 或 shell hook。
- 不让外部二进制透明改写命令。

落地方式：

- 先写 [output-budget-policy.md](../../method-forge/docs/method/output-budget-policy.md)。
- 后续如需工具化，只能做显式调用的只读 wrapper。
- wrapper 必须保留原始日志路径，不能吞掉失败上下文。

### coleam00/Archon

可吸收价值：

- YAML DAG 把开发流程拆成确定性节点。
- PIV loop: Explore -> Plan -> Implement -> Validate。
- Smart PR review: 先按 diff 复杂度分类，再选择 review 维度。
- fresh context / isolated phase 的方法思想。

不直接采用：

- 不安装 Archon。
- 不引入 Archon CLI、Web UI、平台连接或 workflow executor。
- 不重做 Codex 原生 worktree、PR、subagent 或 background task。

落地方式：

- 写成 [workflow-presets.md](../../method-forge/docs/method/workflow-presets.md)。
- 只作为 `method-forge` orchestration preset 的设计参考。

### mattpocock/skills

可吸收价值：

- `diagnose`: 先构造反馈环，再复现、假设、插桩、修复、回归。
- `tdd`: 一个行为一个测试，按 vertical slice 做 red-green-refactor。
- `grill-with-docs`: 用代码和文档澄清术语、边界与 ADR。
- `improve-codebase-architecture`: 查找浅模块、测试困难、接口过宽。
- `zoom-out`: 在局部代码前先建立模块地图。

不直接采用：

- 不原样安装 Claude skills。
- 不复制 Claude 命令命名。
- 不把交互式 grilling 变成长问卷。

落地方式：

- 将诊断/TDD/架构审查规则补进现有 `method-forge` skill 与模板。
- 只在复杂或高风险任务触发，不增加轻任务负担。

### forrestchang/andrej-karpathy-skills

可吸收价值：

- Think before coding.
- Simplicity first.
- Surgical changes.
- Goal-driven verification.

当前状态：

- 这些原则已基本进入全局规则和 `codex-enhanced-system`。

补足方式：

- 在 `plan-review` 增加隐含假设和原生能力优先检查。
- 在 `verify` 增加目标可追溯性检查。

### luongnv89/claude-howto

可吸收价值：

- 以功能目录方式梳理 commands、skills、subagents、hooks、memory。
- 帮助建立 Claude 生态概念到 Codex App 原生能力的映射。

不直接采用：

- 不复制 `.claude/` 目录。
- 不将 Claude hooks / agents / commands 配置迁移到 Codex。

落地方式：

- 作为兼容性映射参考。
- 若后续写 onboarding 文档，只引用概念分类，不导入实现。

## Adaptation Package

本轮方案包包含：

- `docs/research/github-ai-workflow-adaptation-2026-05-02.md`
- `method-forge/docs/method/workflow-presets.md`
- `method-forge/docs/method/output-budget-policy.md`
- `method-forge/docs/templates/plan-review-template.md` 小补项
- `method-forge/docs/templates/verify-template.md` 小补项
- `method-forge/README.md` 索引补充
- `method-forge/docs/method/workflow.md` 引用补充

## Acceptance Criteria

- 没有安装外部项目。
- 没有新增运行时依赖。
- 没有启用 hook、daemon、proxy 或 background runner。
- 没有覆盖 Codex 原生能力边界。
- 所有新增内容都以“补足 method-forge 方法层”为定位。
