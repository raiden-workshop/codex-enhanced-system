# Intake

## Request Summary

- request: Implement the research-to-adaptation package while strictly preserving existing functionality and preferring Codex native capabilities.
- requester: user
- workspace: `/Users/wz/project/codex-enhanced-system`
- date: 2026-05-02

## Classification

| Field | Value |
| --- | --- |
| task_type | `complex-change` |
| risk_level | `medium` |
| need_spec | `true` |
| need_research | `false` |
| need_memory_lookup | `true` |
| suggested_path | `spec-flow` |
| next_step | Implement method-layer additions only. |

## Goal

- primary_goal: Add concrete method-forge support for the approved external workflow adaptation plan.
- success_signal: New behavior is represented as additive docs/templates/skill guidance, with no runtime deployment and no replacement of Codex native features.

## Constraints And Signals

- hard_constraints: Do not install external projects; do not enable hooks; do not replace Codex native features; do not cover existing method-forge paths.
- dependencies: Existing method-forge docs, templates, and skill contracts.
- known_risks: A new workflow concept could accidentally become a second platform if not bounded.

## Reasoning

### Why This Task Type

- The work spans docs, templates, skill contracts, and a new skill.

### Why This Risk Level

- Medium risk because method-forge is a shared workflow layer and incorrect routing rules could affect future tasks.

### Research Or Memory Notes

- Prior research package identified `rtk`, `Archon`, Matt Pocock skills, Karpathy guidelines, and claude-howto as method inputs only.
- Existing memory and repo rules require Codex-native capability boundaries to remain authoritative.

