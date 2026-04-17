# Spec / 规格

## Scope / 范围

- 为仓库新增一个 GitHub Actions workflow，至少覆盖：
  - `/Users/wz/project/knowledge-base/tests/test_kb_query.py`
  - `/Users/wz/project/knowledge-base/kb maintain --json`
  - `/Users/wz/project/knowledge-base/kb drift-review --json`
- 为当前线程创建一个 active heartbeat automation，用于恢复或继续 `method-forge` autonomous run。
- 记录实际验证结果与最终状态。

- Add one GitHub Actions workflow that covers at least:
  - `/Users/wz/project/knowledge-base/tests/test_kb_query.py`
  - `/Users/wz/project/knowledge-base/kb maintain --json`
  - `/Users/wz/project/knowledge-base/kb drift-review --json`
- Create one active heartbeat automation for the current thread to resume or continue `method-forge` autonomous runs.
- Record the actual verification results and final status.

## Non-Goals / 非目标

- 不在本轮引入复杂矩阵 CI、缓存优化或多语言测试扩展。
- 不重写 `method-forge` 规则本身，只把前面已经定稿的规则真正接上运行入口。

- Do not introduce complex matrix CI, cache optimization, or broader multi-language checks in this slice.
- Do not rewrite `method-forge` rules again; only connect the already-approved rules to a real runtime entry point.
