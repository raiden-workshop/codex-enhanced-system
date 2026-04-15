# Consumer AGENTS Rules Snippet

- 所有非闲聊、非纯问答请求默认先产出 `intake.md`。
- 中等及以上复杂度、跨文件、边界不清或风险较高的请求，必须先走 `spec -> plan -> plan-review -> tasks` 再进入实现。
- 任何实质性变更完成后，必须补 `verify.md`；“代码写完了”不等于“交付完成了”。
- 高风险改动可在 `verify` 前追加 `code-review.md`。
- `verify.md` 可以提出 `memory-candidate.md`，但不得直接写长期 memory。
- 失败回退时优先修订原真相源，不新增平行的 `final-v2` 式文档分支。
- 当用户表达“开始落地代码”“开始实现”“开始写代码”“继续写代码”等实现意图时，默认进入 `method-forge` autonomous mode，除非用户明确要求不要自动、先别写代码或只做方案。
- autonomous mode 使用 Codex 原生 heartbeat automation 作为监听者，其内层默认执行引擎为 `method-forge-execute`。
- 不要把单个微切片或一次 `verify` 通过误记为 `completed`；若同一用户目标下下一安全切片已明确，应保持 `running` 并自动推进。 / Do not mark the run `completed` just because a single micro-slice or one `verify` pass finished; if the next safe slice inside the same user goal is already known, keep it `running` and continue automatically.
- research 和 knowledge-base 只作为输入，不替代 `spec.md`、`plan.md` 或 `tasks.md`。
- 会话内流程编排统一叫 `orchestrations`；`automations` 只指 Codex App 原生后台任务。
- 不重复实现 Codex 原生的 multi-agent、worktrees、diff review、git/PR、background automations、sandbox/approvals、skill loading。
