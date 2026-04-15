# Verify / 验证

## Commands / 验证命令

```bash
python3 -m unittest <repo-root>/knowledge-base/tests/test_kb_query.py
python3 <repo-root>/knowledge-base/kb maintain
python3 <repo-root>/knowledge-base/kb maintain --json
python3 <repo-root>/knowledge-base/kb maintain --json --write-report --dry-run
git diff --check -- <repo-root>/knowledge-base/kb <repo-root>/knowledge-base/tests/test_kb_query.py <repo-root>/knowledge-base/KB_COMMANDS.md <repo-root>/docs/specs/2026-04-11-kb-maintain-json
python3 ~/.codex/scripts/refresh_memory.py --workspace-root <repo-root>
```

## Results / 结果

- `unittest`: `Ran 11 tests ... OK`
- `kb maintain`: 文本输出仍正常，当前仓库 `issues: none`
- `kb maintain --json`: 返回 `status / counts / issue_counts / issues`
- `kb maintain --json --write-report --dry-run`: 额外返回 `report_path` 与 `report_action`
- `git diff --check`: 无输出，目标文件格式通过
- `refresh_memory.py`: 成功刷新 workspace memory

- `unittest`: `Ran 11 tests ... OK`
- `kb maintain`: text output remains healthy and the current repository still reports `issues: none`
- `kb maintain --json`: returns `status / counts / issue_counts / issues`
- `kb maintain --json --write-report --dry-run`: additionally returns `report_path` and `report_action`
- `git diff --check`: no output, so the target files passed the formatting check
- `refresh_memory.py`: workspace memory refresh completed successfully

## Conclusion / 结论

- `maintain` 现在具备和 `query` 类似的结构化出口，后续 automation 或 review 流可以直接消费。
- `maintain` now has a structured exit similar to `query`, so later automation or review flows can consume it directly.
