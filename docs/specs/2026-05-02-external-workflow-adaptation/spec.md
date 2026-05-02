# Spec

## Goal

Implement additive method-forge support for the approved external workflow adaptation package.

## User Value

The user can benefit from useful ideas in external AI workflow projects without adding new runtime platforms, losing Codex-native behavior, or creating parallel systems.

## In Scope

- Add a `method-forge-diagnose` skill for bug/regression feedback-loop discipline.
- Add a `diagnosis.md` template.
- Add `diagnose-first` as an intake route for bug/regression requests.
- Connect native-capability and traceability checks into plan review.
- Connect output evidence and traceability checks into verify.
- Update method docs and indexes so future users can find the additions.
- Preserve all existing direct/spec/research/autonomous paths.

## Out Of Scope

- Installing `rtk`, `Archon`, Claude skills, or any external project.
- Enabling shell hooks, Codex hooks, daemons, proxies, or command rewrite.
- Replacing Codex native subagents, worktrees, git/PR, automations, hooks, skill loading, or memories.
- Deploying anything.
- Changing memory-system or knowledge-base implementation.

## Constraints

- All changes must be additive and method-layer only.
- Existing method-forge functionality must remain valid.
- The implementation must be reviewable as Markdown and skill metadata changes.

## Acceptance Criteria

- `method-forge-diagnose` exists with valid `SKILL.md` frontmatter.
- `diagnosis-template.md` exists.
- `diagnose-first` route is documented in intake, execute, and orchestration rules.
- Plan review requires native-capability and traceability checks.
- Verify requires output evidence and traceability checks.
- README and workflow docs index the new additions.
- Validation confirms Markdown links, skill frontmatter, shell syntax, and whitespace.

## Open Questions

- none blocking

