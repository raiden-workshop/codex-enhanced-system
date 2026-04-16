# Resume Rules

## 1. 目的

resume 规则用于让 autonomous 执行在暂停、中断或报错后，能够从文档状态恢复，而不是从头猜。

恢复时也要保持简单：优先从最小、最明确的真相源继续，不额外扩张范围。

## 2. 恢复入口

每次恢复都先读：

1. `runtime/run-state.md`
2. `package-index.md`
3. 当前阶段主文档
4. 最近一次 cycle report

## 3. 恢复决策

### 3.1 如果 `status=completed`

- 不再继续实现
- 只允许做轻量确认或收尾状态同步
- 这里的 `completed` 只应用在顶层任务真正完成时；若只是一个微切片完成且下一安全切片已知，状态应保持 `running`
- `completed` here is reserved for a truly finished top-level task; if only one micro-slice is done and the next safe slice is already known, the status should stay `running`

### 3.2 如果 `status=waiting-human`

- 不自动继续
- 保留 `next_action` 与 `stop_reason`

### 3.3 如果 `status=waiting-external`

- 仅在外部条件满足后恢复
- 未满足前不要盲重试

### 3.4 如果 `status=blocked`

- 先检查 loop guard 是否已经触发上限
- 若只是一次性故障且未触发上限，可重试一次受控步骤
- 若错误签名重复，则保持 `blocked`

### 3.5 如果 `status=running`

- 从 `current_step` 继续
- 若 `current_step` 缺失，则用 `last_success_step` 与 `package-index.md.next_step` 推导

## 4. 恢复时的下一步选择

优先级如下：

1. `run-state.md.next_action`
2. `package-index.md.current_phase`
3. 最近失败的步骤回退点
4. `method-forge-execute` 的重新判断

## 5. 恢复时必须更新的字段

恢复成功或失败后，都应更新：

- `last_resumed_at`
- `current_step`
- `retry_count`
- `last_error_signature`
- `next_action`
- `stop_reason`

## 6. 不允许的恢复方式

- 忽略 `run-state.md` 直接重新从头跑
- 忽略 `blocked` / `waiting-human` 状态继续实现
- 只在聊天里说明恢复，不更新文档状态
