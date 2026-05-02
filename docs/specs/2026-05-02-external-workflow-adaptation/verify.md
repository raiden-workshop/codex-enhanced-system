# Verify

## Change Summary

- Added `method-forge-diagnose` and `diagnosis-template.md`.
- Added `diagnose-first` routing for bug/regression requests.
- Connected native-capability, traceability, and output evidence checks into existing method-forge skills and templates.
- Updated method docs and README indexes.

## Status

| Field | Value |
| --- | --- |
| behavior_check | `pass` |
| test_check | `pass` |
| regression_risk | `low` |
| doc_sync_needed | `completed` |
| memory_candidate | `no` |
| final_status | `passed` |

## Behavior Validation

- The implementation is additive and method-layer only.
- Existing direct/spec/research/autonomous paths remain documented.
- Codex-native ownership remains explicitly preserved.
- No external project was installed or deployed.

## Test Validation

- `git diff --check`: pass
- `bash -n scripts/bootstrap.sh scripts/install-skills.sh`: pass
- skill frontmatter check: pass
- local Markdown link check: pass

## Regression Risk

- Low. The changes are Markdown and skill instruction changes.
- Main residual risk is future overuse of `diagnose-first`; this is mitigated by limiting it to bug/regression requests without a reliable feedback loop.

## Traceability Check

- Every changed file maps to the user goal: yes.
- Unrelated edits avoided: yes.
- Existing Codex-native capability preserved: yes.

## Output Evidence

- command: `git diff --check`
- status: pass
- summary: no whitespace errors
- raw evidence: terminal output was empty with exit code 0
- missing: none

- command: `bash -n scripts/bootstrap.sh scripts/install-skills.sh`
- status: pass
- summary: shell syntax valid
- raw evidence: terminal output was empty with exit code 0
- missing: none

- command: skill frontmatter check
- status: pass
- summary: all method-forge skill directories contain frontmatter-bearing `SKILL.md`
- raw evidence: `skill frontmatter ok`
- missing: none

- command: local Markdown link check
- status: pass
- summary: all local Markdown links resolve
- raw evidence: `markdown links ok`
- missing: none

## Documentation Sync

- README updated.
- Workflow docs updated.
- Skill contracts updated.
- Template lint rules updated.
- Research-to-adaptation report already present.

## Memory Candidate

- eligible: no
- candidate_summary:
- why_stable:
- why_not: This is implementation evidence for a specific repository change, not a reusable cross-project memory rule.

## Open Issues

- none

