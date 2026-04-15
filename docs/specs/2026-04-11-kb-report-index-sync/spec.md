# Spec / 规格

## Goals / 目标

- 让 command-generated reports 在写入后立即成为 index graph 的有效成员，而不是新的治理噪音来源。
- Ensure command-generated reports become valid members of the index graph immediately after writing instead of turning into new governance noise.

- 让 `maintain` 和 `drift-review` 的写后摘要反映最终状态，而不是停留在写前计数或遗漏 index 收口。
- Make the post-write summaries of `maintain` and `drift-review` reflect the final state instead of keeping pre-write counts or skipping index closeout.

## Non-Goals / 非目标

- 不扩展新的 maintenance 或 drift heuristics
- 不自动把新 report 推进到 `hot.md` 或 `overview.md`
- 不改动 report 内容本身的业务结论

- Do not add new maintenance or drift heuristics
- Do not auto-promote new reports into `hot.md` or `overview.md`
- Do not change the business conclusions inside the reports themselves

## Functional Rules / 功能规则

- 实际执行 `--write-report` 时，应自动把新 report 写入 `wiki/index.md` 对应 section
- 若 index 发生实际写入，应同步刷新 `wiki/index.md` 的 `updated_at`
- `maintain --write-report` 的摘要应基于写后重新计算的 counts/issues
- `drift-review --write-report` 的写后状态不应引入新的 maintenance residue
- `--dry-run` 保持为非修改式预览

- On a real `--write-report`, the command should auto-register the new report under the correct section of `wiki/index.md`
- If the index changes, the command should also refresh `wiki/index.md`'s `updated_at`
- The `maintain --write-report` summary should use post-write recomputed counts and issues
- The post-write state of `drift-review --write-report` should not introduce fresh maintenance residue
- `--dry-run` remains a non-mutating preview
