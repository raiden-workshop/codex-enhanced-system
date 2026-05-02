# Workflow

## 1. 目标

`method-forge v1` 定义一条适配 Codex App 的最小 spec-driven workflow：

- 让请求先被标准化，再被实现
- 让复杂任务有稳定的文档真相源
- 让质量门发生在实现前后，而不是只在收尾时补救
- 让 memory 与 knowledge-base 只在合适的位置介入

默认遵循同一组工作原则：先想清楚再写、简单优先、只做必要改动、先定义成功标准再验证。

## 2. 推荐产物包

本 workspace 只提供方法与模板，不强制消费方采用固定目录。

推荐每个复杂变更建立一个独立文档包，例如：

```text
docs/specs/<change-id>/
├── intake.md
├── spec.md
├── plan.md
├── plan-review.md
├── diagnosis.md
├── tasks.md
└── verify.md
```

轻任务至少保留：

- `intake.md`
- `verify.md`

如果要把这套方法层接到别的 workspace，上述目录约定的轻量落地方式见：

- [docs/method/consumer-adoption.md](consumer-adoption.md)
- [docs/presets/minimal-change-package/README.md](../presets/minimal-change-package/README.md)
- [docs/method/workflow-presets.md](workflow-presets.md)

## 3. 主流程

### 3.1 路由入口

所有非闲聊请求先进入 `feature-intake`，目标是回答一件事：

- 接下来应该直接实现、先 research，还是进入完整 spec 流

### 3.2 复杂任务流

标准复杂任务主流程如下：

```text
feature-intake
-> spec-clarify
-> plan-write
-> plan-review
-> task-breakdown
-> implement
-> verify-change
```

适用场景：

- 多文件改动
- 需求边界不清
- 存在明显回归风险
- 需要跨知识来源研究
- 需要把实现交给其他 worker 或后续执行者

### 3.3 轻任务流

轻任务可以走短路径：

```text
feature-intake
-> implement
-> verify-change
```

适用场景：

- 单点修复
- 明确且低风险的文档改动
- 不需要复杂设计和拆任务的请求

### 3.3.5 诊断优先流

bug、失败、性能退化或不稳定行为优先走诊断路径：

```text
feature-intake
-> diagnose
-> implement or spec-flow
-> verify-change
```

适用场景：

- 当前没有可靠复现路径
- 可见症状可能不是根因层
- 修复前需要先明确测试缝隙或正确修复层

### 3.4 `v1.5` 可选增强流

高风险或高复用价值任务可以在主流程后挂接扩展质量门：

```text
implement
-> code-review
-> verify-change
-> memory-promote
```

说明：

- `code-review` 不是每次必跑，但高风险改动推荐启用
- `memory-promote` 只在 `verify.md` 已经认定 candidate 合格时运行
- 输出较长的验证命令遵循 [output-budget-policy.md](output-budget-policy.md)，先压缩对话内容，但保留可追溯证据

## 4. 每个阶段的进入与退出条件

### 4.1 Intake

进入条件：

- 收到原始请求

退出条件：

- 已明确 `task_type`
- 已明确 `risk_level`
- 已明确 `suggested_path`
- 已明确 `next_step`

### 4.2 Spec

进入条件：

- `intake.md` 判定 `need_spec=true`

退出条件：

- `goal`、`scope`、`constraints`、`acceptance_criteria` 稳定
- 技术细节尚未过早展开

### 4.3 Plan

进入条件：

- `spec.md` 稳定，可以作为技术设计真相源

退出条件：

- 已说明触点、顺序、风险、测试与 rollout
- 其他执行者可以基于 `plan.md` 开始拆任务

### 4.4 Plan Review

进入条件：

- `plan.md` 已完成

退出条件：

- 明确 `approved` 或 `needs-revision`
- 明确遗漏测试、过度设计、顺序问题和歧义
- 明确是否误重复了 Codex 原生能力
- 明确计划改动是否能追溯到用户目标

### 4.5 Tasks

进入条件：

- `plan-review.md` 为 `approved`

退出条件：

- 每个任务都能独立执行与验证
- 依赖关系明确

### 4.6 Verify

进入条件：

- 已有实际变更结果

退出条件：

- 明确行为是否达标
- 明确测试是否达标
- 明确文档是否已同步
- 明确是否只够资格成为 memory candidate
- 明确长输出验证证据是否可追溯

### 4.6.5 Diagnosis

进入条件：

- `intake.md` 标记 `suggested_path=diagnose-first`

退出条件：

- 已建立反馈环或说明阻塞原因
- 已记录可证伪假设和证据
- 已明确根因、正确修复层和回归测试计划

### 4.7 Code Review

进入条件：

- 高风险改动已完成，或用户明确要求 review

退出条件：

- 已给出 `approved`、`needs-fix` 或 `advisory-only`
- findings 与缺失测试都已记录

### 4.8 Memory Promote

进入条件：

- `verify.md` 标记 `memory_candidate=yes`

退出条件：

- 已得到可交接的 `memory-candidate.md`
- 未直接写入长期 memory

## 5. 研究、知识库与 memory 的位置

### 5.1 Research / Knowledge Base

它们可以作为以下阶段的输入：

- `feature-intake`
- `spec-clarify`
- `plan-write`

它们不能替代以下产物：

- `spec.md`
- `plan.md`
- `tasks.md`

### 5.2 Memory

`method-forge` 不直接写长期 memory。

只有当 `verify.md` 认定某条结论满足以下条件时，才允许提出 memory candidate：

- 已验证
- 稳定
- 可复用
- 可压缩
- 对当前或跨 workspace 工作方式有帮助

## 6. 人工确认边界

`v1` 推荐以下人工确认点：

- `spec.md` 完成后
- `plan.md` 完成后
- `plan-review.md` 为 `needs-revision` 时

这不是在复制审批系统，而是在复杂任务上保留可控的暂停点。

## 7. 当前环境修正

参考资料中曾出现“新增工作流扩展优先用 `skills` 和 `automations`”的说法。

在当前最新环境里，必须显式修正为：

- `skills`：能力单元
- `orchestrations`：会话内流程编排
- `automations`：Codex App 原生后台任务
- `lifecycle hooks`：Codex 原生 session / prompt / permission / tool-use 事件触发能力

`method-forge` 只定义 `skills` 与 `orchestrations` 的方法层规则，不重做 automations 或 lifecycle hooks。
