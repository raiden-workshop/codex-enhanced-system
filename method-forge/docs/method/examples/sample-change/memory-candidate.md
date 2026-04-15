# Memory Candidate

## Candidate Summary

- summary: 在当前环境中，会话内流程编排统一命名为 `orchestrations`，`automations` 仅指 Codex App 原生后台任务。
- source_verify_doc: `<repo-root>/method-forge/docs/method/examples/sample-change/verify.md`
- source_change: `method-forge v1 workflow bootstrap`

## Why It Qualifies

- verified_evidence: 该规则已写入 `AGENTS.md`、workflow、orchestration rules 与 3 个 orchestration README，并经本次闭环验证。
- stability_reason: 这是当前环境的最新命名边界，属于跨任务稳定规则。
- reuse_reason: 新 worker、后续文档和 future skills 都会复用这条规则。
- compression_reason: 结论可以压缩为一条简短命名规则，不依赖上下文长文。

## Proposed Scope

| Field | Value |
| --- | --- |
| suggested_scope | `workspace` |
| promotion_status | `candidate-only` |

## Why Not Direct Memory Write

- `method-forge` 只负责提出 candidate，真正晋升仍由现有 memory system 流程决定。

## Exclusions

- what_not_to_promote: 不晋升本次任务的文件清单、一次性验证步骤或样例路径细节。
