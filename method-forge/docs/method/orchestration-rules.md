# Orchestration Rules

## 1. 定义

`orchestrations` 是会话内流程编排规则，不是后台自动任务，不是新的执行平台。

它们只负责：

- 决定下一步该调用哪个 skill
- 保证顺序与停点正确
- 在必要时中止并回退到上一步修订

它们不负责：

- 直接写长期 memory
- 直接实现功能
- 代替 Codex App 原生 automations
- 代替 Codex App 原生 lifecycle hooks

编排规则要保持最小可用：只定义下一步、顺序和停点，不额外发明新的流程层。

## 2. 全局规则

- `feature-intake` 是默认入口
- `plan-review` 在 `plan.md` 产出后默认运行
- `verify-change` 在实质性改动后默认运行
- 高风险改动可在 `verify-change` 前挂接 `code-review`
- 当 `plan-review.approval_status=needs-revision` 时，流程必须回到 `plan-write`
- memory 只能以 candidate 形式从 `verify` 侧提出，不能在 orchestration 中直接写入
- 若需要整理候选，可在 `verify` 之后运行 `memory-promote`，但仍不得直接写 memory

## 3. `route-request`

目标：

- 先做 intake，再把请求送进轻任务流或复杂任务流

顺序：

1. 运行 `method-forge-feature-intake`
2. 如果 `need_research=true`，先补研究输入
3. 如果 `suggested_path=diagnose-first`，先运行 `method-forge-diagnose`
4. 如果 `need_spec=false`，交给直接实现路径
5. 如果 `need_spec=true`，交给 `spec-flow`
6. 无论走哪条实现路径，收尾都要进 `verify-and-memory`

停止条件：

- 请求仍然不清晰，无法得出稳定 `next_step`
- 存在需要用户确认的高风险前提
- bug / regression 请求无法建立反馈环，且缺少继续诊断所需证据

## 4. `spec-flow`

目标：

- 保证复杂任务按 `spec -> plan -> review -> tasks` 顺序推进

顺序：

1. 运行 `method-forge-spec-clarify`
2. 视复杂度决定是否在 `spec.md` 后暂停确认
3. 运行 `method-forge-plan-write`
4. 视复杂度决定是否在 `plan.md` 后暂停确认
5. 运行 `method-forge-plan-review`
6. 若 `needs-revision`，回到 `method-forge-plan-write`
7. 若 `approved`，运行 `method-forge-task-breakdown`

停止条件：

- `spec.md` 仍有关键未决问题
- `plan-review.md` 持续无法通过

## 5. `verify-and-memory`

目标：

- 把“实现完成”转换成“已验证、可交付、可判断是否值得记住”

顺序：

1. 运行 `method-forge-verify-change`
2. 判断行为、测试、风险与文档同步状态
3. 若符合条件，仅提出 memory candidate
4. 若不符合条件，明确阻塞项或后续动作

输出规则：

- `verify.md` 是交付完成的真相源
- memory candidate 只能作为 `verify.md` 的一部分或其派生摘要存在
- 不直接触发长期 memory 写入

可选扩展：

- 高风险改动可先运行 `method-forge-code-review`
- bug、失败、性能退化或不稳定行为可先运行 `method-forge-diagnose`
- 当 `verify.md.memory_candidate=yes` 时，可再运行 `method-forge-memory-promote`

## 6. 最新环境修正

当前环境明确要求：

- 会话内流程编排命名为 `orchestrations`
- `automations` 专指 Codex App 原生后台能力
- `lifecycle hooks` 专指 Codex 原生 session / prompt / permission / tool-use 事件触发能力

因此，任何历史文档里把这两者混用的地方，都应在当前实现中按此规则修正。
