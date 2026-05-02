# Plan

## Summary

Add external workflow adaptation as concrete method-forge guidance while keeping Codex native features as the execution layer.

## Implementation Order

1. Add the diagnosis skill and template.
2. Add `diagnose-first` to intake and execution routing.
3. Update orchestration rules and workflow docs.
4. Update plan-review and verify skill procedures.
5. Update skill contracts and template lint rules.
6. Update README and workflow preset references.
7. Run doc-focused validation.

## Touchpoints

- `method-forge/skills/method-forge-diagnose/SKILL.md`
- `method-forge/docs/templates/diagnosis-template.md`
- `method-forge/docs/templates/intake-template.md`
- `method-forge/docs/templates/package-index-template.md`
- `method-forge/skills/method-forge-feature-intake/SKILL.md`
- `method-forge/skills/method-forge-execute/SKILL.md`
- `method-forge/skills/method-forge-plan-review/SKILL.md`
- `method-forge/skills/method-forge-verify-change/SKILL.md`
- `method-forge/docs/method/orchestration-rules.md`
- `method-forge/docs/method/skill-contracts.md`
- `method-forge/docs/method/template-lint-rules.md`
- `method-forge/docs/method/workflow.md`
- `method-forge/docs/method/workflow-presets.md`
- `method-forge/README.md`

## Risks

- Risk: diagnosis route becomes a mandatory burden for simple fixes.
  Mitigation: keep it optional and only route bug/regression requests without a feedback loop.
- Risk: output budget policy hides important evidence.
  Mitigation: require raw evidence traceability in verify.
- Risk: external project ideas become a second platform.
  Mitigation: explicitly reject runners, hooks, worktree managers, PR platforms, and global command rewriting.

## Test Strategy

- `git diff --check`
- `bash -n scripts/bootstrap.sh scripts/install-skills.sh`
- Check every skill directory has a frontmatter-bearing `SKILL.md`.
- Check local Markdown links resolve.

## Rollout

- No runtime rollout.
- No skill install command run.
- Source changes are ready for later commit/push if requested.

