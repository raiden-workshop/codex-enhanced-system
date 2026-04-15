# KB Commands

`knowledge-base` 现在可以按几个高频命令来维护，不用再背整套流程。

命令入口：

```bash
./kb <command> ...
```

常用别名：

- `search` / `ask` = `query`
- `new` = `add`
- `note` = `log`
- `check` / `lint` = `maintain`
- `drift` = `drift-review`
- `update-index` = `reindex`
- `remove` = `delete`
- `distill` / `promote-memory` = `distill-memory`

## 命令集

### `status`

快速看当前知识库规模。

Quickly inspect the current knowledge-base size.

```bash
./kb status
```

### `query`

查询 canonical knowledge pages，并输出轻量级 provenance 信息。

Search canonical knowledge pages and return lightweight provenance details.

```bash
./kb query "formal memory"
./kb query authority --type concept --limit 3
./kb query "formal memory" --json
./kb query authority --include-reports --no-dedupe
```

说明：

- 默认搜索 `source / entity / concept / synthesis / domain`，不包含 `report`
- `--type` 可以重复传入，用来限制结果类型
- `--include-reports` 可以把 `report` 页一起纳入
- 默认会对明显的语言镜像结果做保守去重；如果想看原始重复项，用 `--no-dedupe`
- 排序会优先更像答案页的类型：`concept / synthesis / entity / domain` 会优先于 `source`，`report` 即使纳入也会降权
- 输出会附带 `source_refs`、`related`，必要时还会显示 `suppressed_duplicates`
- `--json` 适合脚本、自动流程或后续 automation 消费

Notes:

- By default the command searches `source / entity / concept / synthesis / domain`, not `report`
- You can pass `--type` multiple times to narrow the result types
- `--include-reports` adds report pages into the search set
- Conservative locale-mirror dedupe is on by default; use `--no-dedupe` if you want the raw duplicate results
- Ranking now prefers answer-like pages: `concept / synthesis / entity / domain` rank ahead of `source`, while `report` pages are downweighted even when included
- The output includes `source_refs`, `related`, and `suppressed_duplicates` when dedupe collapses mirrors
- `--json` is intended for scripts, automated flows, or later automation consumers

### `add`

新增一个 page scaffold。

```bash
./kb add source --slug my-doc --title "My Doc" --import-from /tmp/my-doc.md --raw-dest raw/inbox/my-doc.md
./kb add concept --slug formal-memory-boundary --title "Formal memory boundary" --source-ref wiki/sources/source-my-doc.md
```

说明：

- `source` 支持直接把外部文件拷进 `raw/`
- 其他类型默认只生成 canonical 模板页
- 新增 canonical page 后现在会自动补进 `wiki/index.md`
- 如果想一步补上结构化日志，可加 `--write-log`
- 新增后建议继续补 `log`，然后跑 `maintain`

### `log`

给 `wiki/log.md` 追加结构化记录。

```bash
./kb log ingest --summary "add source-my-doc" --note "Added wiki/sources/source-my-doc.md" --note "Imported raw/inbox/my-doc.md"
```

说明：

- 实际写入 `wiki/log.md` 时，现在也会同步刷新它自己的 `updated_at`

Notes:

- A real write to `wiki/log.md` now also refreshes its own `updated_at`

### `maintain`

做轻量维护检查。

```bash
./kb maintain
./kb maintain --write-report
./kb maintain --json
```

当前会检查：

- frontmatter 是否存在
- 必要字段是否齐全
- `source/entity/concept/synthesis` 是否缺 `source_refs`
- `source` 的 `source_refs` 是否仍然指向 `raw/`
- `entity/concept/synthesis` 的 `source_refs` 是否仍然落在 `wiki/sources/` 或 `raw/`
- `entity/concept/synthesis` 是否至少保留一个 canonical `wiki/sources/` 支撑页，而不只是 raw 路径
- `source_refs` / `related` 是否出现重复或自指
- 内部链接是否断裂
- canonical 页是否漏进 `wiki/index.md`
- `wiki/index.md` 是否有 stale entry
- `wiki/index.md`、`wiki/overview.md`、`wiki/hot.md`、`wiki/log.md` 这些导航/健康页是否还完整互链
- `wiki/hot.md` 和 `wiki/overview.md` 是否还保留对关键 domain / synthesis / report 健康入口的覆盖
- 文本输出现在会附带 `health_verdict` 和 `issue_groups`，更容易快速判断当前健康状态
- `--json` 可输出结构化 `health_verdict`、`counts`、`issue_counts`、`issue_groups`、`issues` 和 `recommendations`，便于脚本或后续 automation 消费
- `--write-report` 现在会把新生成的 maintenance report 自动补进 `wiki/index.md`，避免写完马上留下新的 index drift

Current checks include:

- whether frontmatter exists
- whether required fields are present
- whether `source / entity / concept / synthesis` pages are missing `source_refs`
- whether `source` page `source_refs` still resolve into `raw/`
- whether `entity / concept / synthesis` page `source_refs` still resolve into `wiki/sources/` or `raw/`
- whether `entity / concept / synthesis` pages still retain at least one canonical `wiki/sources/` support page instead of only raw pointers
- whether `source_refs` or `related` introduce duplicate or self-referential targets
- whether internal links are broken
- whether canonical pages are missing from `wiki/index.md`
- whether `wiki/index.md` contains stale entries
- whether `wiki/index.md`, `wiki/overview.md`, `wiki/hot.md`, and `wiki/log.md` still form a healthy navigation surface
- whether `wiki/hot.md` and `wiki/overview.md` still cover key domain / synthesis / report entry points
- text output now includes `health_verdict` and `issue_groups` so the current health state is easier to scan quickly
- `--json` emits structured `health_verdict`, `counts`, `issue_counts`, `issue_groups`, `issues`, and `recommendations` for scripts or later automation consumers
- `--write-report` now also auto-registers the new maintenance report in `wiki/index.md` so the write does not immediately create fresh index drift

### `drift-review`

做轻量 drift review，专门看“哪些页可能需要复核”，而不是把它们直接当成维护错误。

Run a lightweight drift review that focuses on “which pages may need review,” without treating them as hard maintenance errors.

```bash
./kb drift-review
./kb drift-review --json
./kb drift-review --write-report --dry-run
```

当前会产出这些 drift signals：

- `source-lag`: `entity / concept / synthesis / domain` 早于其 canonical source support 页
- `guide-lag`: `index / overview / hot` 早于它们链接到的 canonical 页
- `metadata-lag`: 例如 `log.md` 的 `updated_at` 早于最新 dated log entry
- `report-lag`: report 层整体早于最新 canonical graph
- 输出会带 `drift_verdict`、`signal_counts`、`signal_groups` 和 `recommendations`
- `--write-report` 可生成 `report-drift-review-<date>.md`，并在实际写入时把报告内容收敛到写入后的最终状态，而不是保留写入前的旧 `report-lag` 快照
- 实际写入时也会把新 report 自动补进 `wiki/index.md`，避免 report 归档本身又制造新的 index drift

Current drift signals include:

- `source-lag`: an `entity / concept / synthesis / domain` page is older than its canonical source support pages
- `guide-lag`: `index / overview / hot` is older than the canonical pages it points to
- `metadata-lag`: for example, `log.md` has an `updated_at` older than the latest dated log entry
- `report-lag`: the report layer as a whole is older than the latest canonical graph
- the output includes `drift_verdict`, `signal_counts`, `signal_groups`, and `recommendations`
- `--write-report` can generate a `report-drift-review-<date>.md`, and an actual write now converges the archived report to the post-write final state instead of preserving a stale pre-write `report-lag` snapshot
- an actual write also auto-registers the new report in `wiki/index.md` so the archive step does not create fresh index drift on its own

### `reindex`

检查或同步 `wiki/index.md`。

```bash
./kb reindex
./kb reindex --write
./kb reindex --write --prune
```

说明：

- 默认只检查
- `--write` 会补上缺失条目
- `--prune` 会移除已经失效的 canonical 条目
- 只要 `reindex` 实际改写了 `wiki/index.md`，现在也会同步刷新 `updated_at`
- 自动补的描述是保守占位文案，之后可以手工润色

### `delete`

安全删除。默认不是硬删，而是移到 `output/trash/`。

```bash
./kb delete wiki/sources/source-old-doc.md
./kb delete wiki/sources/source-old-doc.md --with-raw
```

说明：

- 会顺手移除 `wiki/index.md` 里的对应条目
- 若确实移除了 index 条目，也会同步刷新 `wiki/index.md` 的 `updated_at`
- 如果想一步补上结构化删除记录，可加 `--write-log`
- `--with-raw` 会把 `source_refs` 指向的 raw 文件一起移到 trash
- 删完建议补一条 `log`，再跑一次 `maintain`

### `distill-memory`

把稳定结论蒸馏到 workspace memory candidates，再触发全局 memory refresh。

```bash
./kb distill-memory wiki/syntheses/synthesis-codex-native-memory-governance-baseline.md
./kb distill-memory --fact "跨项目稳定结论：正式长期记忆权威只有 ~/.codex/memory"
```

说明：

- 默认会把结论写到当前 workspace 的 `candidates/reference/`
- 默认会加“跨项目稳定结论”信号，方便后续进入 global candidate 流程
- 默认会调用 `refresh_memory.py`
- 如果你只想先看结果不刷新，用 `--no-refresh`

## 推荐日常流

### 新增知识

```bash
./kb add source ...
./kb reindex --write
./kb log ingest --summary "..." --note "..."
./kb maintain
```

### 删除知识

```bash
./kb delete wiki/sources/source-xxx.md --with-raw
./kb log maintenance --summary "delete source-xxx" --note "Deleted wiki/sources/source-xxx.md"
./kb maintain
```

### 例行维护

```bash
./kb maintain --write-report
./kb reindex --write --prune
```

### 蒸馏到记忆系统

```bash
./kb distill-memory wiki/concepts/concept-formal-memory-authority.md
```

## 命令哲学

- `add` 负责结构化新增
- `log` 负责留下操作轨迹
- `maintain` 负责发现问题
- `reindex` 负责修目录入口
- `delete` 负责安全退场
- `distill-memory` 负责把稳定结论送进 memory candidate 流程

这样你之后可以把知识库当成一个小型内容系统来维护，而不是一套要背诵的文档礼仪。
