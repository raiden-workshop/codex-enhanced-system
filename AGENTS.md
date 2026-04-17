# Codex Enhanced System

- This repository is the consolidated home for the Codex enhancement stack.
- Treat Codex App native capabilities as the source of truth when they overlap with local workflows.
- Read the relevant subdirectory `AGENTS.md` before making changes in `memory-system/` or `method-forge/`.
- If the task is about the knowledge base, switch to `/Users/wz/project/knowledge-base` and read that repo's `AGENTS.md`.
- Keep repository-local docs aligned with the current merged structure and avoid references to retired standalone repo paths.

## Review Guidelines

- When Codex is used for GitHub review, prioritize blocking correctness, security, regression, and data-loss risks first.
- Treat GitHub `@codex review` as a narrow P0/P1-style gate, not as a substitute for the broader `method-forge-code-review` quality pass.
- Do not elevate style-only or wording-only comments into blocking findings unless a more specific local rule says otherwise.
- If the user wants broader maintainability, test-gap, or flow-cleanup review, explicitly run the repository's `method-forge-code-review` path instead of assuming GitHub review already covered it.
