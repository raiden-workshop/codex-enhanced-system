# Tasks

## Task 1

- id: `T1`
- goal: Add diagnosis skill and template.
- files: `method-forge/skills/method-forge-diagnose/SKILL.md`, `method-forge/docs/templates/diagnosis-template.md`
- depends_on: none
- verification: skill frontmatter check and Markdown link check
- done_definition: New skill and template exist and are linked.
- status: done

## Task 2

- id: `T2`
- goal: Add diagnose-first routing.
- files: intake template, feature-intake skill, execute skill, orchestration rules
- depends_on: `T1`
- verification: route appears in template and docs
- done_definition: Bug/regression requests can route to diagnosis before implementation.
- status: done

## Task 3

- id: `T3`
- goal: Make native-capability and traceability checks actionable.
- files: plan-review template, plan-review skill, verify template, verify skill
- depends_on: none
- verification: relevant sections and procedures are present
- done_definition: Checks are represented in both templates and skill procedure.
- status: done

## Task 4

- id: `T4`
- goal: Update docs and indexes.
- files: README, workflow docs, workflow presets, skill contracts, template lint rules
- depends_on: `T1`, `T2`, `T3`
- verification: Markdown link check
- done_definition: Future users can discover and apply the new additions.
- status: done

## Task 5

- id: `T5`
- goal: Verify the change.
- files: repository validation output
- depends_on: `T1`, `T2`, `T3`, `T4`
- verification: `verify.md`
- done_definition: All chosen checks pass and residual risk is recorded.
- status: done

