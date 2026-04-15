---
name: method-forge-autonomous-execution
description: Use when the user says phrases like "开始落地代码", "开始实现", "开始写代码", "继续写代码", or explicitly asks for autonomous execution, background continuation, heartbeat-based continuation, pause or resume of an existing autonomous run, or asks whether method-forge should keep running without restating it every cycle. This skill uses native Codex heartbeat automation as the listener and method-forge-execute as the default inner engine.
---

# method-forge-autonomous-execution

## Purpose

为 `method-forge` 提供自动续跑层。

它不重做调度器，而是规定：

- 谁来监听
- 如何恢复
- 如何默认调用 `method-forge-execute`
- 如何避免死循环

## Use When

- 用户说“开始落地代码”
- 用户说“开始实现”
- 用户说“开始写代码”
- 用户说“继续写代码”
- 用户说“自动执行直到结束”
- 用户说“后台继续跑”
- 用户说“启动 autonomous mode”
- 用户说“用 heartbeat 继续”
- 用户希望任务暂停后能继续
- 用户希望 heartbeat / autonomous 模式自动续跑
- 用户问“后续还要不要再指定 method-forge”
- 当前任务本来就在恢复一个已有的 autonomous run

## Execution Model

- 监听者：Codex 原生 heartbeat automation
- 默认执行引擎：`method-forge-execute`
- 恢复真相源：`run-state.md` + `package-index.md`
- 防循环机制：loop guard

## Procedure

1. 建立或更新变更包。
2. 建立 `runtime/run-state.md`。
3. 通过 Codex App 原生 automation 入口创建或恢复 heartbeat 监听；当实现意图命中时默认应创建，除非用户明确说不要自动、先别写代码或只做方案。若当前环境只需要说明文档，则至少准备 heartbeat automation prompt，明确默认使用 `method-forge-execute`。
4. 每一轮恢复时先读 `run-state.md`、`package-index.md` 和当前阶段文档。
5. 只有在状态允许时才继续推进。
6. 每轮结束更新 `run-state.md` 并写 cycle report。
7. 若触发 loop guard，则转为 `blocked` 或 `waiting-human`，而不是盲重试。
8. 不要把单个微切片或一次 `verify` 通过误记为 `completed`；若同一用户目标下下一安全切片已明确，应保持 `running` 并继续自动推进。 / Do not mark a run `completed` just because a single micro-slice or one `verify` pass finished; if the next safe slice inside the same user goal is already known, keep the run `running` and continue automatically.

## Default Rule

当用户用实现意图短语触发本 skill，或 autonomous 模式已经启动后，后续 heartbeat 周期都不需要用户再次指定“按method-forge执行”。

默认就应当使用 `method-forge-execute`，除非任务已经：

- `completed`
- `blocked`
- `waiting-human`

这里的 `completed` 指顶层任务完成，不是某个微切片刚结束。 / Here `completed` means the top-level task is done, not that one micro-slice just ended.

## Outputs

- `runtime/run-state.md`
- `runtime/reports/<cycle-timestamp>.md`
- 可选 heartbeat automation prompt 草案

## Guardrails

- 不重做 Codex 原生 automation 平台
- 不绕过 `verify`
- 不在重复错误上死循环
- 不直接写长期 memory

## References

- [docs/method/autonomous-execution.md](../../docs/method/autonomous-execution.md)
- [docs/method/resume-rules.md](../../docs/method/resume-rules.md)
- [docs/method/loop-guard-rules.md](../../docs/method/loop-guard-rules.md)
- [docs/templates/run-state-template.md](../../docs/templates/run-state-template.md)
- [docs/templates/autonomous-heartbeat-prompt-template.md](../../docs/templates/autonomous-heartbeat-prompt-template.md)
