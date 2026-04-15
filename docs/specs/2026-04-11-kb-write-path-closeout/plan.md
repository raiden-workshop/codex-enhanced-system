# Plan / 计划

1. 补齐 `cmd_log` 的 metadata 写回语义。
   Fix the metadata writeback semantics of `cmd_log`.

2. 让 `cmd_add` 自动把新 canonical page 纳入 `wiki/index.md`。
   Make `cmd_add` auto-register new canonical pages in `wiki/index.md`.

3. 给 `cmd_add` / `cmd_delete` 增加可选的一步式 `--write-log`。
   Add optional one-step `--write-log` support to `cmd_add` / `cmd_delete`.

4. 补回归测试、命令文档和验证记录。
   Add regression coverage, command docs, and verification records.
