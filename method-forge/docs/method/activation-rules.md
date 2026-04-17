# Activation Rules

## 1. 目标

activation rules 用于把用户的自然语言意图自动映射到 `method-forge` 的正确入口。

特别是当用户说“开始落地代码”这类话时，系统应默认理解为：

- 进入实现阶段
- 默认进入 `method-forge` autonomous mode
- `method-forge-execute` 作为 autonomous 的默认内层执行引擎

这些触发规则应保持简单稳定，只覆盖必须的入口，不额外扩展成新的流程体系。

## 2. 触发优先级

### 2.1 明确指定 `method-forge`

若用户说：

- `按method-forge方式执行`
- `按 method-forge 执行`
- `use method-forge`

则默认触发 `method-forge-execute`。

若同一句里还明确要求“自动执行”“后台继续”“autonomous”“heartbeat 续跑”等，再触发 `method-forge-autonomous-execution`。

### 2.2 表示“开始实现/落地代码”的意图

若用户说：

- `开始落地代码`
- `开始实现`
- `开始写代码`
- `进入实现阶段`
- `继续落地`
- `继续写代码`
- `开始开发`

并且当前线程里已经存在以下任一前置条件：

- 已有需求
- 已有设计草稿
- 已有变更包
- 已有 `spec.md` / `plan.md` / `tasks.md`

则默认触发 **`method-forge-autonomous-execution`**。

### 2.3 明确要求自动续跑，或恢复既有 autonomous run

若用户说：

- `启动 autonomous mode`
- `自动执行直到结束`
- `后台继续跑`
- `用 heartbeat 继续`
- `恢复刚才那个 autonomous run`

或者当前变更包已经存在 `runtime/run-state.md`，并且其状态表明本来就在恢复一个 autonomous run，

则触发 **`method-forge-autonomous-execution`**。

## 3. 为什么默认进 autonomous

这一步恢复为默认进入 autonomous。

原因是用户原本想要的行为就是：当已经表达明确实现意图时，不只是在当前线程里开始写一点代码，而是让 `method-forge` 尽量自动把缺失文档、实现、`verify` 和续跑一起推进。

这并不意味着重做第二套调度器：

- 监听者仍然是 Codex App 原生 heartbeat / background automation
- `method-forge-execute` 仍然是默认内层执行引擎
- 只有当用户明确说不要自动、先别写代码、只做方案，或当前风险过高必须人工确认时，才降级出 autonomous

## 4. 默认行为

当命中上述触发条件时，默认行为是：

1. 先检查当前变更包是否已存在。
2. 若不存在，则创建 `docs/specs/<date>-<slug>/` 和 `package-index.md`。
3. 若缺 `intake/spec/plan/tasks`，则由 `method-forge-execute` 自动补齐。
4. 启用 autonomous 运行态，写入 `runtime/run-state.md`。
5. 通过 Codex App 原生 automation 入口创建或恢复监听。
6. 若已具备实现上下文，则直接开始实现。
7. 实现完成后补 `verify.md`。
8. 后续 heartbeat 周期默认继续调用 `method-forge-execute`。

补充：

- 若同一用户目标下已经存在明确且安全的下一实现切片，不应在某个微切片刚完成后就退出到等待用户再次说“继续”。
- If the same user goal already has a clear and safe next implementation slice, the autonomous run should not drop back to waiting for the user to say “continue” again after just one micro-slice completes.

## 5. 退出或降级条件

以下情况不进入 autonomous：

- 用户明确说 `不要自动`
- 用户明确说 `先别写代码`
- 用户只想做方案，不想实现
- 当前缺关键 repo / workspace 上下文
- 任务风险过高且必须先人工确认

## 6. 在每个 worker 生效的前提

要让这套触发在“每个 worker”里都生效，需要满足两件事：

### 6.1 技能全局可见

至少要让以下入口 skill 对所有 worker 可见：

- `method-forge-execute`
- `method-forge-autonomous-execution`

推荐安装到：

- `~/.codex/skills/` 或 `$CODEX_HOME/skills/`

如果外部资料里看到 `$HOME/.agents/skills`，按旧口径或别名理解即可；当前这套仓库和本地 Codex App 环境统一以 `~/.codex/skills/` 或 `$CODEX_HOME/skills/` 为准。

安装后需要重启 Codex 才能稳定拾取新技能。

### 6.2 触发规则被共享

至少要在消费方 `AGENTS.md` 或共享规则里写入：

- “开始落地代码 / 开始实现 / 开始写代码” 默认进入 `method-forge` autonomous mode
- autonomous 的监听者使用 Codex 原生 heartbeat automation
- autonomous 的默认执行引擎为 `method-forge-execute`
- “不要自动 / 先别写代码 / 只做方案” 等短语可以降级出 autonomous

## 7. 推荐写法

消费方可以在 `AGENTS.md` 使用类似规则：

```text
当用户表达“开始落地代码”“开始实现”“开始写代码”“继续写代码”等实现意图时，默认进入 `method-forge` autonomous mode，除非用户明确要求不要自动、先别写代码或只做方案。
autonomous mode 的监听者使用 Codex 原生 heartbeat automation，内层默认执行引擎为 `method-forge-execute`。
```

## 8. 配套文件

- autonomous 扩展：[docs/method/autonomous-execution.md](autonomous-execution.md)
- autonomous 入口 skill：[skills/method-forge-autonomous-execution/SKILL.md](../../skills/method-forge-autonomous-execution/SKILL.md)
- 消费方 `AGENTS` 草案：[docs/templates/consumer-agents-rules-template.md](../templates/consumer-agents-rules-template.md)
