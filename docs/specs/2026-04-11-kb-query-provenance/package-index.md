# Package Index / 变更包索引

## Change / 变更信息

- change_id: `2026-04-11-kb-query-provenance`
- title: `knowledge-base query command with lightweight provenance`
- owner: `Codex`
- workspace: `<repo-root>`
- date: `2026-04-11`

## Status / 状态

| Artifact | Status | Path |
| --- | --- | --- |
| intake | `done` | `docs/specs/2026-04-11-kb-query-provenance/intake.md` |
| spec | `done` | `docs/specs/2026-04-11-kb-query-provenance/spec.md` |
| plan | `done` | `docs/specs/2026-04-11-kb-query-provenance/plan.md` |
| plan-review | `done` | `docs/specs/2026-04-11-kb-query-provenance/plan-review.md` |
| tasks | `done` | `docs/specs/2026-04-11-kb-query-provenance/tasks.md` |
| implementation | `done` | `knowledge-base/kb`, `knowledge-base/tests/test_kb_query.py` |
| verify | `done` | `docs/specs/2026-04-11-kb-query-provenance/verify.md` |
| code-review | `not-applicable` | |
| memory-candidate | `not-applicable` | |
| run-state | `done` | `docs/specs/2026-04-11-kb-query-provenance/runtime/run-state.md` |
| autonomous-cycle-report | `not-applicable` | |
| workflow-health-report | `not-applicable` | |

## Summary / 摘要

- goal: 为 `knowledge-base` 落地一个可运行的 `query/search/ask` 查询入口，并附带基础出处信息。
- goal_en: Land a working `query/search/ask` command for `knowledge-base` with basic provenance output.
- current_phase: `completed`
- current_phase_en: `completed`
- next_step: 在下一轮继续补 query 健康检查、结果去重和更强的 provenance lint。
- next_step_en: In the next slice, extend query health checks, result dedupe, and stronger provenance linting.

## Notes / 备注

- 本轮只实现第一批最小闭环，不包含向量检索、自动 citation 重写或 page evolution 自动化。
- This round ships the first minimal vertical slice only; it does not include vector search, automatic citation rewriting, or page-evolution automation.
