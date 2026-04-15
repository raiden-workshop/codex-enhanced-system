# Loop Guard Rules

## 1. 目的

loop guard 规则用于防止 autonomous 执行在同一步骤上无限重试或在没有进展时持续循环。

## 2. 推荐保护项

### 2.1 单步最大重试次数

- `max_step_retries: 3`

同一个 `current_step` 超过上限后，状态改为 `blocked`。

### 2.2 重复错误指纹

- `max_same_error_repeats: 2`

同一错误签名连续出现时，不继续盲重试。

### 2.3 无进展周期数

- `max_no_progress_cycles: 2`

连续多个周期没有文档更新、状态推进或验证结果变化时，应停机。

### 2.4 总周期预算

- `max_total_cycles_per_task: 12`

超过预算后转为 `waiting-human` 或 `blocked`。

### 2.5 高风险停机

遇到以下情况必须停：

- 需求变化
- 缺少关键上下文
- 破坏性操作
- verify 长期不过
- memory candidate 可能覆盖现有稳定规则

## 3. 错误指纹

推荐把错误压缩成短签名，例如：

- `missing-repo-context`
- `tests-failing-same-stack`
- `spec-ambiguity-core-scope`
- `permission-blocked`

## 4. 触发停机后的动作

触发 loop guard 后至少更新：

- `status`
- `stop_reason`
- `last_error_signature`
- `human_confirmation_needed`
- `next_action`

并生成新的 cycle report。

## 5. 默认建议

在没有项目特定规则时，默认使用本文件中的建议阈值。

如果消费方项目风险更高，可以在自己的 workspace 提高保守性，但不要去掉 loop guard。
