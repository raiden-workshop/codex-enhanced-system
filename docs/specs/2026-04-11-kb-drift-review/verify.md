# Verify / 验证

## Commands / 验证命令

```bash
python3 -m unittest /Users/wz/project/knowledge-base/tests/test_kb_query.py
python3 /Users/wz/project/knowledge-base/kb drift-review
python3 /Users/wz/project/knowledge-base/kb drift-review --json
python3 /Users/wz/project/knowledge-base/kb drift-review --write-report --dry-run
git diff --check -- /Users/wz/project/knowledge-base/kb /Users/wz/project/knowledge-base/tests/test_kb_query.py /Users/wz/project/knowledge-base/KB_COMMANDS.md <repo-root>/docs/specs/2026-04-11-kb-drift-review
python3 ~/.codex/scripts/refresh_memory.py --workspace-root <repo-root>
```

## Results / 结果

- `unittest`: `Ran 17 tests ... OK`
- `drift-review`: 当前仓库返回 `review-needed`，共 `warn=6`、`info=3`
- `drift-review --json`: 返回了 `drift_verdict`、`signal_counts`、`signal_groups`、`signals`、`recommendations`
- `drift-review --write-report --dry-run`: 返回了待写入的 drift review report 路径
- `git diff --check`: 无输出，目标文件格式通过
- `refresh_memory.py`: 成功刷新 workspace memory

- `unittest`: `Ran 17 tests ... OK`
- `drift-review`: the current repository returns `review-needed` with `warn=6` and `info=3`
- `drift-review --json`: returns `drift_verdict`, `signal_counts`, `signal_groups`, `signals`, and `recommendations`
- `drift-review --write-report --dry-run`: returns the drift-review report path that would be written
- `git diff --check`: no output, so the target files passed the formatting check
- `refresh_memory.py`: workspace memory refresh completed successfully

## Conclusion / 结论

- `drift-review` 已经不仅是新命令，而且能在真实仓库中识别出一批值得复核的页面。
- `drift-review` is not merely a new command; it already identifies a real set of pages worth reviewing in the live repository.
