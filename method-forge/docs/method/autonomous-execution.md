# Autonomous Execution

## 1. 目标

`autonomous-execution` 扩展用于让一个任务在启动后，尽量由 Codex 自动推进到本轮任务结束，同时具备：

- 可恢复
- 可停止
- 可监控
- 不死循环

推进时保持同一组默认原则：先想清楚再做、简单优先、只做必要改动、先定义成功标准再验证。

## 2. 核心模型

这层扩展遵守现有边界：

- **Codex 原生 heartbeat / background automation**
  负责“监听”和“回来继续执行”
- **Codex 原生 lifecycle hooks**
  负责 session、prompt、permission、tool-use 等即时事件前后触发，不负责跨回合续跑
- **`method-forge-execute`**
  负责“本轮应该做什么”
- **变更包文档**
  负责“做到哪了、下一步是什么”

一句话：

- 原生 automation 是监听器
- 原生 hooks 是即时事件触发面
- `method-forge-execute` 是默认执行引擎
- `run-state.md` 和 `package-index.md` 是恢复真相源

## 2.1 hooks 与 heartbeat 的边界

- hooks 适合 `SessionStart`、`UserPromptSubmit`、`PermissionRequest`、`PreToolUse`、`PostToolUse`、`Stop` 这类事件的轻量检查、提示或审计。
- heartbeat / background automation 适合跨回合恢复、周期性读取 `run-state.md`、继续推进任务。
- autonomous mode 不应把 hooks 当作第二套调度器，也不应通过 hooks 绕过 loop guard、approval 或 `verify`。

补充边界：

- 当用户表达“开始落地代码”“开始实现”“开始写代码”“继续写代码”等实现意图时，默认启用这层扩展
- 若用户明确说不要自动、先别写代码或只做方案，可降级为当前线程里的 `method-forge-execute`
- 恢复既有 autonomous run 时，也继续启用这层扩展

## 3. 是否还要重复指定 `method-forge`

不用每次重复指定。

当 autonomous 模式已经启动后，每一次 heartbeat 周期都应默认先使用 `method-forge-execute` 作为内层执行引擎，除非：

- `run-state.md` 已标记为 `completed`
- `run-state.md` 已标记为 `blocked`
- `run-state.md` 已标记为 `waiting-human`
- 当前周期只需要做状态整理而不是继续推进

也就是说：

- **启动时** 你可以直接说“开始落地代码”“开始实现”“继续写代码”，系统就默认进入 autonomous mode
- **显式启动时** 你也可以直接说“启动 autonomous mode”
- **后续自动续跑时** 不需要你每轮再重复指定

## 4. 推荐运行时结构

推荐把 autonomous 运行态放在当前变更包下：

```text
docs/specs/<change-id>/
├── package-index.md
├── intake.md
├── spec.md
├── plan.md
├── plan-review.md
├── tasks.md
├── verify.md
└── runtime/
    ├── run-state.md
    └── reports/
        └── <cycle-timestamp>.md
```

## 5. 真相源优先级

autonomous 周期恢复时应按以下顺序读取：

1. `runtime/run-state.md`
2. `package-index.md`
3. 当前阶段主文档，例如 `plan.md`、`tasks.md`、`verify.md`
4. 最近一次 cycle report

恢复时不要依赖聊天上下文猜测状态。

## 6. 单次 heartbeat 周期的默认动作

每一轮 heartbeat 默认做以下动作：

1. 读取 `run-state.md` 与 `package-index.md`
2. 检查 loop guard 是否已触发停机条件
3. 判断当前状态是 `running`、`blocked`、`waiting-human` 还是 `completed`
4. 若可继续，调用 `method-forge-execute` 作为默认引擎
5. 推进一个或多个安全步骤，直到完成、阻塞、需要人类确认或达到本轮预算
6. 更新 `run-state.md`
7. 更新 `package-index.md`
8. 写一份新的 cycle report

这套周期行为的前提是：该 automation 已经由实现意图触发、显式 autonomous 请求触发，或当前 run 明确处于恢复状态。

补充一条关键约束：

- 不要把“某个微切片刚完成 `verify`”误当成整个任务已经 `completed`。若同一用户目标下的下一安全切片已经明确，状态应保持 `running`，并把 `current_step` / `next_action` 推进到下一切片继续自动执行。
- Do not treat “one micro-slice just passed `verify`” as the whole task being `completed`. If the next safe slice within the same user goal is already known, keep the status `running` and advance `current_step` / `next_action` so execution continues automatically.

## 7. 允许的停止状态

`run-state.md.status` 允许以下字面量：

- `running`
- `blocked`
- `waiting-human`
- `waiting-external`
- `completed`
- `aborted`

其中：

- `blocked` 表示当前无法自动继续
- `waiting-human` 表示必须人工确认
- `waiting-external` 表示依赖外部系统、权限或输入
- `completed` 表示本轮任务已结束
- `completed` 只表示当前顶层任务或当前变更包目标已经结束，不表示单个微切片刚刚结束
- `completed` only means the current top-level task or change-package goal is finished; it does not mean a single micro-slice has just finished

## 8. 自动推进与人工确认边界

可以自动继续的情况：

- 只是缺少标准化文档，需要补 `intake/spec/plan/tasks/verify`
- 已有 plan，当前只是按既定任务实现
- 已有 verify 阻塞项，且阻塞项可由当前 repo 上下文独立解决

应暂停的情况：

- 需求边界发生实质变化
- 连续失败且错误指纹重复
- 需要破坏性操作或高风险变更
- 缺少关键上下文、权限或外部输入

## 9. 当前边界

这层扩展仍然不做：

- 重做 Codex 原生 automation 调度器
- 重做 Codex 原生 lifecycle hook runner
- 直接写长期 memory
- 跳过 `verify`
- 为了自动化而绕过 loop guard

## 10. 配套文件

- 恢复规则：[docs/method/resume-rules.md](resume-rules.md)
- 防死循环规则：[docs/method/loop-guard-rules.md](loop-guard-rules.md)
- 运行态模板：[docs/templates/run-state-template.md](../templates/run-state-template.md)
- 周期报告模板：[docs/templates/autonomous-cycle-report-template.md](../templates/autonomous-cycle-report-template.md)
- heartbeat prompt 草案：[docs/templates/autonomous-heartbeat-prompt-template.md](../templates/autonomous-heartbeat-prompt-template.md)
