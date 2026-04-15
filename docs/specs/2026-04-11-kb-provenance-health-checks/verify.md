# Verify / 验证

## Commands / 验证命令

```bash
python3 -m unittest <repo-root>/knowledge-base/tests/test_kb_query.py
python3 <repo-root>/knowledge-base/kb maintain
git diff --check -- <repo-root>/knowledge-base/kb <repo-root>/knowledge-base/tests/test_kb_query.py <repo-root>/knowledge-base/KB_COMMANDS.md <repo-root>/docs/specs/2026-04-11-kb-provenance-health-checks
python3 ~/.codex/scripts/refresh_memory.py --workspace-root <repo-root>
```

## Results / 结果

- `unittest`: `Ran 9 tests ... OK`
- `kb maintain`: `issues: none`
- `git diff --check`: 无输出，目标文件格式通过
- `refresh_memory.py`: 成功刷新 workspace memory

- `unittest`: `Ran 9 tests ... OK`
- `kb maintain`: `issues: none`
- `git diff --check`: no output, so the target files passed the formatting check
- `refresh_memory.py`: workspace memory refresh completed successfully

## Conclusion / 结论

- provenance lint 与 guide-surface health check 已接入默认维护流程，且当前仓库在新规则下保持通过。
- Provenance lint and guide-surface health checks are now part of the default maintenance flow, and the current repository still passes under the new rules.
