# Flowdoc

Flowdoc is a CLI tool that converts **semantic HTML** documents into **dyslexia-friendly, readable HTML** that works consistently across devices and print.

Why Flowdoc? Many documents are technically "readable" but visually fatiguing for dyslexic readers due to cramped line length, spacing, and layout choices. Flowdoc deliberately **throws away layout fidelity** and re-renders content with typography and spacing tuned for readability.

## v1 scope (summary)

- Input: HTML with semantic structure (headings, paragraphs, lists)
- Output: a single, self-contained HTML file (no external CSS/fonts/scripts/images)
- Readability over fidelity: no attempt to preserve original styling or branding
- Optional font toggle: `--font opendyslexic` (not default)

Full boundaries: see `SCOPE.md`.

## Status

Planning complete; implementation not started.

## Planned CLI

```bash
flowdoc convert input.html
flowdoc convert input.html -o output.html
flowdoc convert input.html --font opendyslexic
```

Print to PDF: open the output in a browser and use print-to-PDF.

## Documentation

- `SCOPE.md` - frozen v1 product boundaries and success criteria
- `docs/decisions.md` - authoritative implementation/test spec (contracts + invariants)
- `docs/ARCHITECTURE.md` - locked v1 implementation choices (runtime, libraries, module structure, pipeline, testing)
- `docs/0_0_FLOWDOC_V1_PLAN.md` - execution checklist for v1
- `docs/research_typography_guidelines.md` - typography research/reference
- `docs/architecture_exploration.md` - non-normative historical exploration/background
- `ABOUT.md` - project origin story and motivation

## License

MIT
