# Flowdoc Program Board

## Identity (Frozen)

Flowdoc is a free, open-source CLI tool that converts semantic prose HTML
into accessible, self-contained, printable HTML for readers with dyslexia
and related conditions. For parents, teachers, SEN coordinators, and
accessibility practitioners.

## v1 Success Definition

- >=90% of the 10-fixture corpus produces clean article content (no leading junk, no trailing boilerplate, no structural artifacts).
- Output is byte-identical across repeated runs and across supported extraction modes.
- On at least 3 representative complex pages, Flowdoc output is qualitatively preferred over browser Reader Mode.

## Primary User Hypothesis

Target users are parents, teachers, SEN coordinators, and accessibility
practitioners who currently reformat documents manually. No institutional
buyer dependency. Validation through direct community feedback.

## Primary Beneficiary

Readers with dyslexia or similar reading-comprehension friction who benefit from controlled typography and structured prose.

## Current Milestone

Corpus expansion -- v1 definition deferred until corpus results are in.

## Phase 2 Exit Criteria

- Guardian and Ringer either (a) fail explicitly and cleanly or (b) extract correct article body.
- No trailing boilerplate (Related, Share, Republish, navigation blocks) in any fixture.
- No structural artifacts (e.g., stray "FORM removed", "[-]" in inappropriate places).
- Titles and opening paragraphs are preserved when present in source.
- No orphan trailing sections.
- Determinism preserved across extraction mode flag.
- No regression on currently clean fixtures.
- Niggle inventory is exhausted for the v1 fixture set (all recorded artifacts are either fixed or explicitly accepted as known limitations).

## Phase 2 Status

Complete. All exit criteria met. Identity10 evaluation: 8 PASS, 1 MARGINAL, 2 FAIL.

## Phase 3 — Ship v1

**Step 1 -- Corpus expansion session** *(next dedicated session)*
Expand test fixtures beyond Identity10 and Eval20. More document types, styles,
and sources. Diagnose Wikipedia failure -- fixable or architectural boundary.
Results determine v1 definition.

**Step 2 -- Print validation** *(needs dedicated planning)*
Requires thought before execution. Questions to resolve:
- Which document types represent real use cases?
- What are we evaluating -- typography, layout, readability, page breaks?
- Who is assessing -- owner alone, or a dyslexic reader?
- What is pass/fail criteria?

Primary reviewer candidate: owner's son. Selection of documents and evaluation
criteria to be agreed before printing anything.

**Step 3 -- Define "done" for the engine**
Explicit, measurable, agreed criteria before corpus results come in. Without this
the engine work has no natural stopping point.

**Step 4 -- Define v1**
Based on corpus results, print validation, and "done" definition. Rewrite
program-board.md Phase 3 tasks against real data.

**Step 5 -- OpenDyslexic embedding**
Contained, spec'd work. Implement before any public release. Not a current
priority.

**Step 6 -- Hosted reference surface**
Build after engine is stable and v1 is defined. Temporary domain for early
testing. URL input required. Basic typography controls included.
Note: temporary domain (aglet.club) for early testing only -- not the permanent
home.

**Step 7 -- PyPI package**
Clean API, well-documented. Enables community surfaces. Architecture and code
review by human contacts before release.

**Step 8 -- Tester recruitment**
Warm introductions via NSPCC network and personal connections. After hosted
surface exists -- nothing to test before then.

## Top Backlog (Ranked)

1. Trafilatura configuration experiments (baseline vs precision vs fast).
   Completion Criteria: Extraction modes implemented; summary runner compares all 10 fixtures; no default behavior change.

2. Niggle inventory + burn-down plan.
   Completion Criteria: Single consolidated artifact list created; issues classified (boundary / model / sanitization); prioritized remediation plan agreed.

3. Deterministic tail boilerplate trimming.
   Completion Criteria: Trailing CMS artifacts removed without breaking clean fixtures; covered by regression tests.

4. Intro/title recovery improvements (top-section extraction refinement).
   Completion Criteria: Titles and opening paragraphs preserved where present; no new leading junk introduced; covered by regression tests.

5. Orphan trailing section detector + structural artifact cleanup.
   Completion Criteria: No empty or heading-only trailing sections; placeholders used only where intentional; no regressions.

6. Lightweight preview runner for real-user testing.
   Completion Criteria: Simple local viewer for 5 curated demo pages; usable for qualitative feedback sessions.

## Explicitly Out of Scope (v1)

- JS execution / SPA rendering
- Browser extension
- Hosted SaaS
- PDF/DOCX input
- Site-specific extractor registry
- ML-based extraction
- Visual rendering engine
