# Codex Global Memory System QA

日期：2026-04-03

## 自动化测试

执行：

```bash
python3 -m py_compile "<repo-root>/memory-system/scripts/refresh_strict_original_memory.py" "<repo-root>/memory-system/tests/test_refresh_strict_original_memory.py"
python3 "<repo-root>/memory-system/tests/test_refresh_strict_original_memory.py"
```

结果：

- `py_compile` 通过
- `unittest` 9/9 通过

覆盖点：

- durable 候选先入 `candidates`，再 promotion
- `user` 记忆走 global 层，不再落 workspace active
- 问句型 project 记忆被拦截
- 内容哈希避免 `confirmed` 类标题撞车
- 参考记忆每来源 promotion 上限生效
- runtime context 只看焦点 session
- 跨 workspace 的全局反馈冲突能进入 `global/conflicts/open`
- 历史 workspace 记忆会保守回填 `source_workspaces` / `source_runs`
- promoted / duplicate / overflow 的 global candidates 会归档到 `global/candidates_archive/`

## 真实运行验证

执行 1：

```bash
python3 ~/.codex/scripts/refresh_memory.py --workspace-root "<repo-root>/memory-system" --force --force-dream
```

结果摘要：

- `matching_sessions=0`
- `processed=0`
- `dream.ran=true`
- `global_dream.ran=true`
- `global_dream.promoted_writes=2`
- `global_dream.stale=22`
- `global_dream.index_lines=9`

说明：

- 这次真实运行把历史上误晋升的 noisy global references 降级为 `stale`，全局热路径明显变干净。

执行 2：

```bash
python3 ~/.codex/scripts/refresh_memory.py --workspace-root "<repo-root>/memory-system"
```

真实新 run 样本：

- `~/.codex/sessions/2026/04/03/session-memory-system-qa-20260403.jsonl`

结果摘要：

- `matching_sessions=1`
- `processed=1`
- `metadata_migrated.workspace_updates=90`
- `touched_types=["project"]`
- `created_memories=1`
- `global_dream.ran=false`

说明：

- 这次 run 成功生成了 `runs/memory-system-<workspace-key>/session-memory-system-qa-20260403/`
- 新 session 被正确提升成 workspace project memory
- `active_context.md` 也已经按这次 run 重建

## 关键产物检查

已检查：

- `~/.codex/memory/global/runtime/global_context.md`
- `~/.codex/memory/global/memories/MEMORY.md`
- `~/.codex/memory/global/dream/reports/20260403T005754Z.md`
- `~/.codex/memory/workspaces/memory-system-<workspace-key>/runtime/active_context.md`
- `~/.codex/memory/runs/memory-system-<workspace-key>/session-memory-system-qa-20260403/summary.md`
- `~/.codex/memory/workspaces/memory-system-<workspace-key>/memories/project/2026-04-03-dac37a9107c8-codex-app-qa.md`

当前状态：

- `global_context.md` 只保留 2 条全局 feedback，没有再把噪音 reference 带进热路径
- `global MEMORY.md` 只保留 active feedback 索引
- 最新 global dream report 明确记录了 22 条 stale 降级
- `memory system` workspace 的 `active_context.md` 可正常重建
- 新 run 的 `summary.md`、`handoff.md`、`extracted.json` 都已生成
- 新 run 的项目事实已进入 workspace `project` active memory

## QA 结论

本轮实现可用，且比上一版更接近“全局稳定层少而准、workspace 层负责项目真相、run 层只存临时态”的目标。

当前没有阻塞性问题。后续最值得继续跟进的是：

1. 如果后面继续复制 workspace 历史，最好在复制动作本身就携带 `source_workspaces`，不要完全依赖事后迁移
2. 如果未来要保留更多全局 reference，需要再设计更强的 reference 质量门槛与 retention 策略
