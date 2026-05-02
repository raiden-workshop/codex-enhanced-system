# Workflow Presets

## 1. Purpose

`workflow-presets` 是 `method-forge` 对外部 workflow 思路的轻量吸收层。

它不是执行引擎，不是 YAML runner，也不是新平台。它只回答：

- 什么时候选哪条 `method-forge` 路径。
- 哪些质量门应开启。
- 哪些 Codex 原生能力应直接复用。

## 2. Native-First Rule

任何 preset 都必须先走原生能力优先检查：

| Capability | Owner |
| --- | --- |
| subagents / parallel work | Codex App native |
| worktree isolation | Codex App native |
| diff review | Codex App native |
| git / commit / PR | Codex App native |
| heartbeat / background automations | Codex App native |
| lifecycle hooks | Codex App native |
| skill loading | Codex App native |

`method-forge` preset 只能补足方法层顺序、停点和验收。

## 3. Preset: PIV Loop

来源参考：Archon PIV loop。

适用：

- 用户要做中等及以上复杂度功能。
- 需求有明显设计空间。
- 需要先对齐边界再实现。

映射到 `method-forge`：

```text
Explore
-> feature-intake
-> spec-clarify
-> plan-write
-> plan-review
-> task-breakdown
-> implement
-> code-review optional
-> verify-change
```

补足规则：

- Explore 阶段先读代码和现有文档，再问问题。
- 不把 Explore 变成固定长问卷。
- 当用户明确说只做方案时，停在 `plan-review` 或 `tasks`，不进入实现。

## 4. Preset: Idea To Verified Change

来源参考：Archon idea-to-pr。

适用：

- 用户给出自然语言想法，希望变成可交付改动。
- 不一定要求 PR，但要求完整验证。

映射到 `method-forge`：

```text
feature-intake
-> spec-flow
-> implement
-> verify-and-memory
```

补足规则：

- PR、branch、push 仍由 Codex 原生 Git/GitHub 能力处理。
- `method-forge` 只产出计划、任务、verify 和可选 memory candidate。
- 若用户没有要求发布，不默认 push 或部署。

## 5. Preset: Smart Review

来源参考：Archon smart PR review。

适用：

- 用户要求 review。
- 变更面大小不确定。
- 不希望每次都跑重型全量审查。

分类规则：

- `trivial`: 只改拼写、格式、单行说明。
- `small`: 1-3 个文件，逻辑直接，无跨模块影响。
- `medium`: 4-10 个文件，有状态、错误路径或测试影响。
- `large`: 10 个以上文件，或涉及架构、数据、权限、部署。

review 维度按需启用：

- Correctness: 默认启用。
- Error handling: 触及异常、异步、外部 IO 或失败路径时启用。
- Test coverage: 触及源代码时启用。
- Comment quality: 新增或修改注释、docstring、JSDoc 时启用。
- Docs impact: 影响公开 API、命令、配置、用户可见行为时启用。

映射到 `method-forge`：

```text
scope
-> classify
-> method-forge-code-review
-> verify-change
```

## 6. Preset: Diagnose

来源参考：mattpocock/skills `diagnose`。

适用：

- 用户报告 bug、失败、性能退化或不稳定行为。

步骤：

```text
feedback-loop
-> reproduce
-> hypotheses
-> instrument
-> fix
-> regression-test
-> cleanup
-> verify-change
```

实现入口：

- [method-forge-diagnose/SKILL.md](../../skills/method-forge-diagnose/SKILL.md)
- [diagnosis-template.md](../templates/diagnosis-template.md)

硬规则：

- 没有反馈环，不进入猜测式修复。
- 插桩必须带唯一前缀，完成后删除。
- 若无法构造反馈环，明确列出已尝试项和需要的外部证据。

## 7. Preset: TDD Slice

来源参考：mattpocock/skills `tdd`。

适用：

- 用户明确要求 TDD。
- 高风险行为需要先锁定回归。

步骤：

```text
one behavior
-> one failing test
-> minimal implementation
-> pass
-> next behavior
-> refactor only when green
```

硬规则：

- 不一次性写完全部测试再实现。
- 测试应覆盖公共接口和可观察行为，不绑定私有实现细节。

## 8. Rejection Rules

以下内容不得作为 preset 引入：

- 外部 workflow executor。
- 新的后台调度器。
- 新的 worktree 管理层。
- 新的 PR 平台或 review UI。
- 自动安装 hook 的脚本。
- 透明改写 shell 命令的全局配置。
