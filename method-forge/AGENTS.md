# method-forge Rules

- 开工前先读共享 memory guides；重要工作完成后运行 `python3 ~/.codex/scripts/refresh_memory.py --workspace-root "$(git rev-parse --show-toplevel)"`。
- 本 workspace 只实现方法层，不重复实现 Codex App 原生的 multi-agent、worktrees、diff review、git/PR、background automations、sandbox/approvals、skill loading。
- 会话内流程编排统一叫 `orchestrations`；`automations` 只指 Codex App 原生后台任务。
- 本文件只放硬规则；解释性内容一律放到 `docs/method/`。
- 所有非闲聊、非纯问答请求默认先产出 `intake.md`。
- 中等及以上复杂度、跨文件、边界不清或风险较高的请求，必须先走 `spec -> plan -> plan-review -> tasks` 再进入实现。
- 任何实质性变更完成后，必须补 `verify.md`；“代码写完了”不等于“交付完成了”。
- 失败回退时优先修订原真相源，不新增平行的 `final-v2` 式文档分支。
- `verify.md` 可以提出 memory candidate，但不得直接写长期 memory，也不得改造 memory system。
- knowledge base 和 research 只作为输入，不替代 `spec.md`、`plan.md` 或 `tasks.md`。
- 默认使用 Markdown 模板、短小章节和可 diff 的文档组织；不要引入大而全外部框架目录。

## Coding Principles

- Think before coding: surface ambiguity and state assumptions when the risk is real.
- Simplicity first: choose the smallest stable solution.
- Surgical changes: touch only what the request requires.
- Goal-driven execution: define success criteria up front, then verify the result.

## Method Forge Autonomous Coding

- 当用户表达“开始落地代码”“开始实现”“开始写代码”“继续写代码”“进入实现阶段”等实现意图时，默认进入 `method-forge` autonomous mode，除非用户明确要求不要自动、先别写代码或只做方案。
- autonomous mode 使用 Codex 原生 heartbeat / background automation 作为监听者，不重做第二套调度器。
- autonomous mode 的内层默认执行引擎是 `method-forge-execute`；在 autonomous 已经启动后，后续续跑周期不需要用户再次指定“按 method-forge 执行”。
- 若当前任务还没有标准变更包，先建立 `docs/specs/<change-id>/`、`package-index.md` 和 `runtime/run-state.md`。
- 若已有需求或设计草稿，先由 `method-forge-execute` 归一化为 `intake/spec/plan/tasks`，再进入实现。
- 实现完成后必须产出 `verify.md`；高风险改动可在 verify 前追加 `code-review.md`。
- 若 `verify.md` 认为存在稳定可复用结论，只能提出 `memory-candidate.md`，不得直接写长期 memory。
- autonomous mode 必须执行 loop guard：同一步最多重试 3 次，同一错误签名最多重复 2 次，连续无进展最多 2 轮，单任务最多 12 个周期。
- 不要把单个微切片或一次 `verify` 通过误记为 `completed`；若同一用户目标下下一安全切片已明确，应保持 `running` 并自动推进。 / Do not mark the run `completed` just because a single micro-slice or one `verify` pass finished; if the next safe slice inside the same user goal is already known, keep it `running` and continue automatically.
- 触发 `blocked`、`waiting-human`、`waiting-external` 或 `completed` 后必须停止自动推进，并在 `run-state.md` 写明 `stop_reason` 与 `next_action`。
