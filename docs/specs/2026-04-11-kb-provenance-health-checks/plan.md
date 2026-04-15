# Plan / 计划

1. 在 `knowledge-base/kb` 里补 provenance 质量 lint 与 guide-surface health-check helper。
   Add provenance-quality lint and guide-surface health-check helpers in `knowledge-base/kb`.

2. 更新 `check_maintenance()`，把新规则接入默认维护检查。
   Update `check_maintenance()` so the new rules run in the default maintenance pass.

3. 补充单测，覆盖通过场景、弱 provenance 场景和 hot-path 漂移场景。
   Add unit tests covering the passing case, weak-provenance case, and hot-path drift case.

4. 更新双语命令文档并完成验证。
   Update bilingual command docs and finish verification.
