# Flowdoc

Flowdoc is a free, open-source CLI tool that converts web articles into clean, accessible, self-contained HTML files styled for readers with dyslexia and related conditions. It strips site chrome, extracts article content, and produces a single portable document with BDA-recommended typography -- printable, offline-readable, and ready to hand to a student or email to a teacher.

Many documents are technically "readable" but visually fatiguing for readers with dyslexia due to cramped line length, poor spacing, and layout choices that prioritize appearance over readability. Browser Reader Mode helps but is ephemeral -- you cannot save it, print it with controlled typography, or share it reliably. Flowdoc produces actual documents.

## v1 scope (summary)

- Input: HTML with semantic structure (headings, paragraphs, lists)
- Output: a single, self-contained HTML file (no external CSS/fonts/scripts/images)
- Readability over fidelity: no attempt to preserve original styling or branding
- Optional font toggle: `--font opendyslexic` (not default)

Full boundaries: see [SCOPE.md](SCOPE.md).

## Status

Phase 2 complete. Core pipeline built and tested against 11 real-world fixtures (8 clean passes, 1 marginal, 2 known limitations). Preparing for v1 open-source release.

## Planned CLI

```bash
flowdoc convert input.html
flowdoc convert input.html -o output.html
flowdoc convert input.html --font opendyslexic
```

Print to PDF: open the output in a browser and use print-to-PDF.

## Documentation

- [SCOPE.md](SCOPE.md) - frozen v1 product boundaries and success criteria
- [docs/decisions.md](docs/decisions.md) - authoritative implementation/test spec (contracts + invariants)
- [docs/architecture.md](docs/architecture.md) - locked v1 implementation choices (runtime, libraries, module structure, pipeline, testing)
- [docs/flowdoc-v1-plan.md](docs/flowdoc-v1-plan.md) - execution checklist for v1
- [docs/flowdoc-v1-success-contract.md](docs/flowdoc-v1-success-contract.md) - locked v1 success contract (takes precedence over all other docs where conflicts exist)
- [docs/research_typography_guidelines.md](docs/research_typography_guidelines.md) - typography research/reference
- [flowdoc-elevator-pitch.md](flowdoc-elevator-pitch.md) - what Flowdoc is in 60 seconds
- [docs/flowdoc-project-summary.md](docs/flowdoc-project-summary.md) - project history and context
- [ABOUT.md](ABOUT.md) - project origin story and motivation

## License

[MIT](LICENSE)
