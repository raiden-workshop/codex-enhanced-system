# Package Index / 变更包索引

## Change / 变更信息

- change_id: `2026-04-11-kb-report-index-sync`
- title: `knowledge-base report index sync`
- owner: `Codex`
- workspace: `<repo-root>`
- date: `2026-04-11`

## Status / 状态

| Artifact | Status | Path |
| --- | --- | --- |
| intake | `done` | `docs/specs/2026-04-11-kb-report-index-sync/intake.md` |
| spec | `done` | `docs/specs/2026-04-11-kb-report-index-sync/spec.md` |
| plan | `done` | `docs/specs/2026-04-11-kb-report-index-sync/plan.md` |
| plan-review | `done` | `docs/specs/2026-04-11-kb-report-index-sync/plan-review.md` |
| tasks | `done` | `docs/specs/2026-04-11-kb-report-index-sync/tasks.md` |
| implementation | `done` | `knowledge-base/kb`, `knowledge-base/tests/test_kb_query.py`, `knowledge-base/KB_COMMANDS.md` |
| verify | `done` | `docs/specs/2026-04-11-kb-report-index-sync/verify.md` |
| code-review | `not-applicable` | |
| memory-candidate | `not-applicable` | |
| run-state | `done` | `docs/specs/2026-04-11-kb-report-index-sync/runtime/run-state.md` |

## Summary / 摘要

- goal: 让 `maintain --write-report` 和 `drift-review --write-report` 在实际写入新 report 时自动把它补进 `wiki/index.md`，避免写入动作自己制造新的 index drift。
- goal_en: Make `maintain --write-report` and `drift-review --write-report` auto-register new reports in `wiki/index.md` so the write itself does not create fresh index drift.
- current_phase: `completed`
- current_phase_en: `completed`
- next_step: 如有需要，可继续检查其他会修改 `wiki/index.md` 的命令是否也应统一更新 `updated_at` 语义。
- next_step_en: If needed, continue by checking whether other commands that mutate `wiki/index.md` should share the same `updated_at` semantics.

## Notes / 备注

- 本轮把 report 写入后的 index 收口做成了共享能力，并让写后摘要反映最终状态。
- This slice turns post-write report registration into a shared capability and makes the write summaries reflect the final state.
