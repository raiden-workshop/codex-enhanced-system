# Verify / 验证

## Commands / 验证命令

```bash
python3 -m unittest <repo-root>/knowledge-base/tests/test_kb_query.py
python3 <repo-root>/knowledge-base/kb maintain
python3 <repo-root>/knowledge-base/kb drift-review
python3 <repo-root>/knowledge-base/kb maintain --write-report --dry-run
python3 <repo-root>/knowledge-base/kb drift-review --write-report --dry-run
git diff --check -- <repo-root>/knowledge-base/kb <repo-root>/knowledge-base/tests/test_kb_query.py <repo-root>/knowledge-base/KB_COMMANDS.md <repo-root>/docs/specs/2026-04-11-kb-report-index-sync
python3 ~/.codex/scripts/refresh_memory.py --workspace-root <repo-root>
```

## Results / 结果

- `unittest`: `Ran 19 tests ... OK`
- `kb maintain`: `health_verdict: healthy`
- `kb drift-review`: `drift_verdict: stable`
- `kb maintain --write-report --dry-run`: 预览写入 `wiki/reports/report-maintenance-2026-04-11.md`
- `kb drift-review --write-report --dry-run`: 预览写入 `wiki/reports/report-drift-review-2026-04-11-2.md`
- `git diff --check`: 无输出，目标文件与变更包格式通过
- `refresh_memory.py`: 成功刷新 workspace memory

- `unittest`: `Ran 19 tests ... OK`
- `kb maintain`: `health_verdict: healthy`
- `kb drift-review`: `drift_verdict: stable`
- `kb maintain --write-report --dry-run`: previewed a write to `wiki/reports/report-maintenance-2026-04-11.md`
- `kb drift-review --write-report --dry-run`: previewed a write to `wiki/reports/report-drift-review-2026-04-11-2.md`
- `git diff --check`: no output, so the target files and change package passed the formatting check
- `refresh_memory.py`: workspace memory refresh completed successfully

## Conclusion / 结论

- command-generated reports 现在会在写入路径里自动收口到 `wiki/index.md`，不会再因为归档动作本身留下新的 index drift。
- Command-generated reports now close themselves into `wiki/index.md` on the write path, so the archival step no longer leaves behind fresh index drift by itself.
