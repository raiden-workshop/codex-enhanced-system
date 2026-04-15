# Consumer AGENTS Rules Snippet

- 所有非闲聊、非纯问答请求默认先产出 `intake.md`。
- 中等及以上复杂度、跨文件、边界不清或风险较高的请求，必须先走 `spec -> plan -> plan-review -> tasks` 再进入实现。
- 任何实质性变更完成后，必须补 `verify.md`。
- 高风险改动可在 `verify` 前追加 `code-review.md`。
- `verify.md` 可以提出 `memory-candidate.md`，但不得直接写长期 memory。
- 会话内流程编排统一叫 `orchestrations`；`automations` 只指 Codex App 原生后台任务。
- 不重复实现 Codex 原生的 multi-agent、worktrees、diff review、git/PR、background automations、sandbox/approvals、skill loading。
