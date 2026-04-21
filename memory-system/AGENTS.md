# memory system 工作区说明

- 当前子工作区专门维护 Codex App 的全局记忆系统。
- 这里不是业务项目，而是记忆系统本身的设计与实现项目。
- 当前 workspace 对应的全局记忆节点必须先通过 `~/.codex/memory/workspaces/index.json` 按 workspace path 查找；不要硬编码 workspace key。
- 本工作区维护的是受治理的 `~/.codex/memory/`；Codex App 原生 memories `~/.codex/memories/` 不在这里直接实现或改造。

## 开工前先读

- 共享 Guide：
  - `~/.codex/memory/instructions/company/GUIDE.md`
  - `~/.codex/memory/instructions/user/GUIDE.md`
  - `~/.codex/memory/instructions/local/GUIDE.md`
- 当前 workspace Guide：
  - `~/.codex/memory/workspaces/<mapped-workspace-key>/instructions/repo/GUIDE.md`
- 当前 workspace 长期记忆索引：
  - `~/.codex/memory/workspaces/<mapped-workspace-key>/memories/MEMORY.md`
- 当前 workspace 压缩上下文：
  - `~/.codex/memory/workspaces/<mapped-workspace-key>/runtime/active_context.md`

## 完工后补记忆

- 完成重要设计或实现后，运行：

```bash
python3 ~/.codex/scripts/refresh_memory.py --workspace-root "$(git rev-parse --show-toplevel)"
```

## 当前原则

- `worker-run` 只保留临时态，不直接作为正式长期记忆。
- `workspace` 是项目长期记忆主层。
- `global` 只保留跨 workspace 稳定成立的长期记忆。
- 先升 `workspace`，再按规则升 `global`。
- 当 Codex App native memories 已开启时，受治理的 `~/.codex/memory/` 不再拥有 `user` / `feedback` recall；这两类默认关闭并归档，由 `~/.codex/memories/` 负责。

## Coding Principles

- Think before coding: surface ambiguity and state assumptions when the risk is real.
- Simplicity first: choose the smallest stable solution.
- Surgical changes: touch only what the request requires.
- Goal-driven execution: define success criteria up front, then verify the result.

## Method Forge Autonomous Coding

- 当用户表达“开始落地代码”“开始实现”“开始写代码”“继续写代码”“进入实现阶段”等实现意图时，默认进入 `method-forge` autonomous mode，除非用户明确要求不要自动、先别写代码或只做方案。
- autonomous mode 使用 Codex 原生 heartbeat / background automation 作为监听者，不重做第二套调度器。
- autonomous mode 的内层默认执行引擎是 `method-forge-execute`；在 autonomous 已经启动后，后续续跑周期不需要用户再次指定“按 method-forge 执行”。
- 若当前任务还没有标准变更包，先建立 `docs/specs/<change-id>/`、`package-index.md` 和 `runtime/run-state.md`。
- 若已有需求或设计草稿，先由 `method-forge-execute` 归一化为 `intake/spec/plan/tasks`，再进入实现。
- 实现完成后必须产出 `verify.md`；高风险改动可在 verify 前追加 `code-review.md`。
- 若 `verify.md` 认为存在稳定可复用结论，只能提出 `memory-candidate.md`，不得直接写长期 memory。
- autonomous mode 必须执行 loop guard：同一步最多重试 3 次，同一错误签名最多重复 2 次，连续无进展最多 2 轮，单任务最多 12 个周期。
- 不要把单个微切片或一次 `verify` 通过误记为 `completed`；若同一用户目标下下一安全切片已明确，应保持 `running` 并自动推进。 / Do not mark the run `completed` just because a single micro-slice or one `verify` pass finished; if the next safe slice inside the same user goal is already known, keep it `running` and continue automatically.
- 触发 `blocked`、`waiting-human`、`waiting-external` 或 `completed` 后必须停止自动推进，并在 `run-state.md` 写明 `stop_reason` 与 `next_action`。
- 若本文件已有更具体的 memory system 规则，以更具体规则为准，但不得取消 `verify` 或 loop guard。
