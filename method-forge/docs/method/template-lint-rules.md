# Template Lint Rules

## 1. 目的

模板 lint 规则用于保证 `method-forge` 产物：

- 可读
- 可 diff
- 可交接
- 不留空壳章节和假完成状态

## 2. 通用规则

- 不保留未填的占位符含义不明字段
- 枚举值必须使用模板中允许的字面量
- 时间信息优先使用绝对日期
- 一个文件只承载一个主产物，不混放多个阶段的真相源
- 如果某一节不适用，要明确写 `not-applicable` 或一句原因，不要留空
- 若文档引用前序结论，应引用对应文档，不要在本文件里重写一遍

## 3. 分模板检查

### 3.1 `intake.md`

- 必须有 `task_type`、`risk_level`、`need_spec`、`suggested_path`、`next_step`
- `suggested_path` 必须与前文理由一致
- 不得提前展开技术设计

### 3.2 `spec.md`

- 必须同时出现 `in_scope` 与 `out_of_scope`
- `acceptance_criteria` 必须可检验，不能只是愿景描述
- `open_questions` 为空时要明确写无阻塞项

### 3.3 `plan.md`

- 必须包含 `implementation_order`
- 必须覆盖 `test_strategy`
- `out_of_scope` 不能缺失，否则范围容易膨胀

### 3.4 `plan-review.md`

- `findings` 优先于摘要
- 必须有明确的 `approval_status`
- `needs-revision` 时必须指出回退原因

### 3.5 `tasks.md`

- 每个任务都必须有 `verification` 和 `done_definition`
- `depends_on` 不得长期为空；若无依赖，应写 `none`
- 任务数过少时要警惕粒度过大

### 3.6 `verify.md`

- 必须同时给出 `behavior_check` 与 `test_check`
- 若 `test_check=not-run`，必须补残余风险说明
- 若 `memory_candidate=yes`，必须解释为什么稳定且可复用

### 3.7 `code-review.md`

- 若有 findings，必须按严重性排序
- 若无 findings，也要写清残余风险或覆盖盲区

### 3.8 `memory-candidate.md`

- 必须能追溯到来源 `verify.md`
- 必须说明建议作用域与不直接写 memory 的原因
- 不能把一次性任务细节伪装成长期规律

### 3.9 `package-index.md`

- 必须覆盖当前变更包的主要产物状态
- 只做导航，不重复每个文档的全文
- `next_step` 必须和当前状态一致

### 3.10 `workflow-health-report.md`

- 必须给出 `overall_status`、`strongest_signal`、`weakest_signal`
- `actions` 必须可执行，不能只有口号
- 若判定为 `needs-intervention`，必须说明最弱信号和修复方向

### 3.11 `run-state.md`

- `status` 必须使用允许的字面量
- `current_step`、`next_action` 和 loop guard 计数要保持同步
- 若状态为 `blocked` 或 `waiting-human`，必须有 `stop_reason`

### 3.12 autonomous cycle report

- 必须说明 `status_before` 与 `status_after`
- 必须说明本轮是否真的有进展
- 若触发 loop guard，必须记录错误签名和停机理由

## 4. 快速检查清单

- 字段填完整了吗
- 枚举值合法吗
- 是否存在空壳章节
- 是否存在第二真相源
- 是否留下了“后续补上”但没有责任点
