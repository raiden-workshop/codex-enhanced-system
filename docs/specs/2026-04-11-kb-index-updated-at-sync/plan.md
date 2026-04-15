# Plan / 计划

1. 让 `reindex` 改为基于 index page body 重建，并在实际写入时刷新 metadata。
   Make `reindex` rebuild from the index page body and refresh metadata on real writes.

2. 让移除 index 条目的路径也共享同样的 metadata 刷新语义。
   Give the index-entry removal path the same metadata refresh semantics.

3. 补回归测试、命令文档和验证记录。
   Add regression coverage, command docs, and verification records.
