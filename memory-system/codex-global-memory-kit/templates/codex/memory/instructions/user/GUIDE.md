# User Guide

- Use Codex App as the primary AI workspace and avoid unnecessary tool switching.
- Default to the simplest stable path that works.
- When the user says phrases like “开始落地代码”, “开始实现”, “开始写代码”, “继续写代码”, or “进入实现阶段”, default to `method-forge` autonomous mode when the relevant skills are available, unless the user explicitly says not to automate, not to write code yet, or to stay at the planning stage. Use native Codex heartbeat/background automation as the listener and `method-forge-execute` as the default inner engine. Keep loop guards plus `verify` mandatory.
