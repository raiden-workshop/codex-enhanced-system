# Verify / 验证

## Commands / 验证命令

```bash
rg -n "micro-slice|微切片|下一安全切片|top-level task|keep it `running`" <repo-root>/method-forge /Users/wz/project/knowledge-base/AGENTS.md <repo-root>/memory-system/AGENTS.md
git diff --check -- <repo-root>/method-forge/AGENTS.md <repo-root>/method-forge/docs/method/autonomous-execution.md <repo-root>/method-forge/docs/method/activation-rules.md <repo-root>/method-forge/docs/method/resume-rules.md <repo-root>/method-forge/docs/templates/autonomous-heartbeat-prompt-template.md <repo-root>/method-forge/docs/templates/consumer-agents-rules-template.md <repo-root>/method-forge/skills/method-forge-autonomous-execution/SKILL.md /Users/wz/project/knowledge-base/AGENTS.md <repo-root>/memory-system/AGENTS.md <repo-root>/docs/specs/2026-04-11-method-forge-autonomous-continuity
python3 ~/.codex/scripts/refresh_memory.py --workspace-root <repo-root>
```

## Results / 结果

- `rg`: 目标规则已同步到 method-forge 方法文档、skill、模板以及 `knowledge-base` / `memory-system` 的消费方 AGENTS
- `git diff --check`: 无输出，目标文件与变更包格式通过
- `refresh_memory.py`: 成功刷新 workspace memory

- `rg`: the target rule is now present in the method-forge method docs, skill, templates, and the consumer AGENTS for `knowledge-base` and `memory-system`
- `git diff --check`: no output, so the target files and change package passed the formatting check
- `refresh_memory.py`: workspace memory refresh completed successfully

## Conclusion / 结论

- autonomous 的停止粒度现在被明确收敛到“顶层任务完成”，不应再把单个微切片完成误当成需要停机的 `completed`。
- The stopping granularity of autonomous is now explicitly tightened to “top-level task complete,” so a finished micro-slice should no longer be mistaken for a stop-worthy `completed` state.
