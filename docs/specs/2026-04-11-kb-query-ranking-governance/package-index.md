# Package Index / 变更包索引

## Change / 变更信息

- change_id: `2026-04-11-kb-query-ranking-governance`
- title: `knowledge-base query ranking governance and conservative dedupe`
- owner: `Codex`
- workspace: `<repo-root>`
- date: `2026-04-11`

## Status / 状态

| Artifact | Status | Path |
| --- | --- | --- |
| intake | `done` | `docs/specs/2026-04-11-kb-query-ranking-governance/intake.md` |
| spec | `done` | `docs/specs/2026-04-11-kb-query-ranking-governance/spec.md` |
| plan | `done` | `docs/specs/2026-04-11-kb-query-ranking-governance/plan.md` |
| plan-review | `done` | `docs/specs/2026-04-11-kb-query-ranking-governance/plan-review.md` |
| tasks | `done` | `docs/specs/2026-04-11-kb-query-ranking-governance/tasks.md` |
| implementation | `done` | `/Users/wz/project/knowledge-base/kb`, `/Users/wz/project/knowledge-base/tests/test_kb_query.py`, `/Users/wz/project/knowledge-base/KB_COMMANDS.md` |
| verify | `done` | `docs/specs/2026-04-11-kb-query-ranking-governance/verify.md` |
| code-review | `not-applicable` | |
| memory-candidate | `not-applicable` | |
| run-state | `done` | `docs/specs/2026-04-11-kb-query-ranking-governance/runtime/run-state.md` |

## Summary / 摘要

- goal: 收紧 `kb query` 的默认结果质量，让答案型页面优先、`report` 降权，并保守折叠语言镜像重复结果。
- goal_en: Tighten default `kb query` result quality so answer-like pages rank first, `report` pages are downweighted, and locale-mirror duplicates are conservatively collapsed.
- current_phase: `completed`
- current_phase_en: `completed`
- next_step: 继续做 provenance lint 强化和知识页健康检查。
- next_step_en: Continue with stronger provenance linting and knowledge-page health checks.

## Notes / 备注

- 本轮只做查询结果治理，不改 wiki 内容结构，也不引入向量检索。
- This slice only improves query-result governance; it does not change wiki content structure or add vector search.
