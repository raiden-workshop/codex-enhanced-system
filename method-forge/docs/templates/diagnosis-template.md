# Diagnosis

Use this template to turn a bug or regression report into a reproducible feedback loop before fixing.

## Symptom

- user_report:
- observed_behavior:
- expected_behavior:
- affected_scope:

## Feedback Loop

- loop_type:
- command_or_steps:
- status: `reproduced` / `not-reproduced` / `blocked`
- signal_quality: `strong` / `partial` / `weak`
- raw_evidence:

## Hypotheses

| Rank | Hypothesis | Prediction | Evidence | Status |
| --- | --- | --- | --- | --- |
| 1 | | | | `untested` / `supported` / `falsified` |
| 2 | | | | `untested` / `supported` / `falsified` |
| 3 | | | | `untested` / `supported` / `falsified` |

## Instrumentation

- temporary_changes:
- debug_prefix:
- cleanup_status: `not-needed` / `removed` / `pending`

## Root Cause

- cause:
- correct_fix_layer:
- why_not_other_layers:

## Regression Test Plan

- test_seam:
- test_case:
- why_this_covers_the_bug:

## Handoff

- next_path: `direct-implement` / `spec-flow` / `blocked`
- next_step:
- open_questions:

