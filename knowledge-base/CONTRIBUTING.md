# Contributing

This repository is an independent cross-project Markdown knowledge base for Codex workers.

Keep contributions small, traceable, and easy to review.

## Read First

Before making changes, read these files in order:

1. `AGENTS.md`
2. `START_HERE.md`
3. `README.md`
4. `WORKER_HANDOFF.md`
5. `wiki/hot.md`
6. `wiki/domains/domain-codex-native-memory-governance.md`
7. `wiki/reports/report-domain-expansion-readiness-2026-04-09.md` when proposing a new domain

## Contribution Types

Use the GitHub templates for the common workflows:

- `Source Ingest Request`: propose a new source for canonical ingest
- `Domain Expansion Proposal`: propose a second or later domain
- `Knowledge Gap or Drift`: report a missing answer, stale page, or graph drift
- Pull requests: explain canonical impact, review path, and validation

## Core Rules

- Save raw first, then write canonical knowledge
- Do not create canonical conclusions without supporting source pages
- Keep the graph centered on explicit domains, not loose adjacent notes
- Do not add a new domain without checking the domain-expansion-readiness report first
- Do not treat `wiki/reports/` as domain truth
- Do not store secrets, credentials, or sensitive private material in this repository

## Canonical Change Checklist

When a change affects canonical knowledge under `wiki/`:

- Create or update the relevant page under `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/syntheses/`, or `wiki/domains/`
- Update `wiki/index.md`
- Append an entry to `wiki/log.md`
- Update `wiki/overview.md` if the high-level picture changed
- Update `wiki/hot.md` only when the hot path should genuinely change

## Domain Discipline

- Keep one domain stable before expanding into another
- Do not add a second domain just because another project directory exists
- If a new cluster of repeated questions appears, write or update a report first
- Only add `wiki/domains/domain-<slug>.md` after the boundary is clear

## Review Expectations

- Prefer small PRs over broad rewrites
- Quote the exact pages changed in the PR description
- Make it obvious which source pages support any new conclusion
- Call out uncertainty, freshness risks, or overlap with existing pages

## Git Workflow

- Branch from `main`
- Prefer short, intention-revealing commit messages
- Open a PR when the change would benefit from review or when the canonical graph changes materially

## If You Are Unsure

- Start with `wiki/hot.md`
- Prefer opening an issue over making a speculative graph expansion
- Keep the repository cleaner and smaller rather than broader and noisier
