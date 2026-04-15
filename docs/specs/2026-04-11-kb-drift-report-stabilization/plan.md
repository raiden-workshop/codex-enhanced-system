# Plan / 计划

1. 找出 `drift-review --write-report` 把写入前 signals 直接归档的路径。
   Find the path where `drift-review --write-report` archives the pre-write signals directly.

2. 调整写入逻辑，让归档报告和写后摘要都收敛到最终状态。
   Adjust the write path so the archived report and the post-write summary converge to the final state.

3. 补回归测试、命令文档和验证记录。
   Add regression tests, command docs, and verification records.
