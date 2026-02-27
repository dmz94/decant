# Flowdoc Phase 2 Plan

Purpose:
Phase 2 focuses on extraction reliability and deterministic post-processing. No scope expansion beyond program-board.md.

---

## Phase 2A – Extraction Configuration Experiments (Complete)

Status: Complete

- Baseline vs precision vs recall tested.
- Measurement runner implemented.
- Guardrail tests added.
- Baseline remains production default.

No further work unless new fixture evidence justifies it.

---

## Phase 2B – Deterministic Cleanup Heuristics (In Progress)

### 2B.1 Tail Boilerplate Trim
Goal: Remove trailing CMS boilerplate without affecting mid-document content.
Constraint: End-anchored only. Pattern-based. Tests-first.

### 2B.2 Orphan Trailing Section Dropper
Goal: Remove final heading-only sections (0 content blocks).
Constraint: Structural only. No site-specific strings.

Completion Gate:
- No trailing boilerplate in fixture corpus.
- No orphan trailing sections.
- No regression on clean fixtures.
- Determinism preserved.

---

## Phase 2C – Niggle Inventory Session (Next)

Goal:
Capture all remaining structural artifacts across the fixture corpus in one consolidated pass.

Process:
- Run full fixture set.
- Record every artifact.
- Classify into:
  A) Boundary (start/end)
  B) Structural artifact
  C) Sanitization / normalization
- Produce prioritized burn-down list.

Exit:
All recorded artifacts either fixed or explicitly accepted as known limitations.

---

## Phase 2D – Intro/Title Recovery Improvements

Goal:
Improve preservation of titles and opening paragraphs where extraction misses early content.

Constraint:
No site-specific rules.
No fallback cascade changes.

Completion Gate:
- Titles present when available in source.
- Opening paragraphs preserved.
- No new leading junk introduced.

---

## Phase 2E – Lightweight Preview Runner

Goal:
Enable simple qualitative user testing on 5 curated pages.

Scope:
- Local viewer only.
- No SaaS.
- No browser extension.

Completion Gate:
Usable for real-user feedback sessions.

---

## Phase 2 Exit Criteria

- ≥90% clean extraction across fixture corpus.
- No structural artifacts.
- Determinism preserved.
- Niggle inventory exhausted.
- Ready for controlled qualitative user testing.
