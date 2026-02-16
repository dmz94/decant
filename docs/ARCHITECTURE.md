# Flowdoc v1 - Locked Architecture and Tech Stack

**Status:** Locked for v1
**Last Updated:** February 16, 2026

This document locks the v1 implementation choices (runtime, libraries, module layout, pipeline, and testing approach).
These are decisions, not options. Do not re-decide them during implementation.

Authoritative behavior contracts (validation rules, model schema, element handling, CSS invariants, CLI contract) live in [decisions.md](decisions.md).
This document answers "what stack do we use and how is the codebase shaped".

---

## Runtime and distribution (locked)

Runtime:
- Python 3.12+ (floor)

Distribution:
- Dual distribution:
  - pip package for developers: `pip install flowdoc`
  - standalone binaries for Windows/macOS/Linux built with PyInstaller

Rationale (short):
- v1 differentiator is transformation quality and iteration speed, not raw performance.
- Python has the strongest HTML parsing ecosystem for tolerant real-world input.
- Shipping binaries avoids requiring users to install Python.

---

## Selected libraries (locked)

Parser:
- BeautifulSoup4 with the lxml backend

Why:
- Tolerant parsing of imperfect HTML.
- Stable and simple traversal API for DOM-to-model extraction.

Alternatives rejected for v1:
- html5lib backend: more browser-faithful but significantly slower (pure Python).
- lxml-only parsing: faster, but higher friction and less forgiving.

Sanitizer:
- nh3 (Rust-backed, allowlist-based HTML sanitizer)

Why:
- Allowlist-based security model.
- Actively maintained and fast (Rust ammonia backend).
- Clear configuration for tags, attributes, and URL schemes.

Alternatives rejected for v1:
- bleach: deprecated for this use case; avoid depending on html5lib-based sanitization stack.
- lxml.html.clean: blocklist-style and historically problematic for security-sensitive sanitization.

Testing:
- pytest

Why:
- Strong fixtures and parametrization for golden tests.
- Snapshot/plugin ecosystem for model-level tests.

---

## Module structure (locked)

Target layout:

```
flowdoc/
+-- __init__.py              # Public library API
+-- core/
|   +-- constants.py         # Typography values, colors, spacing
|   +-- model.py             # Internal Document Model classes
|   +-- sanitizer.py         # nh3 wrapper with Flowdoc rules
|   +-- content_selector.py  # main -> article -> body selection
|   +-- parser.py            # DOM -> Internal Model transformation
|   +-- degradation.py       # Table/image/form placeholder rules
|   +-- renderer.py          # Model -> HTML + CSS generation
+-- cli/
|   +-- main.py              # CLI wrapper (arg parsing + I/O + exit codes)
+-- io/
    +-- reader.py            # File/stdin reading
    +-- writer.py            # File/stdout writing

tests/
+-- fixtures/
|   +-- input/
|   +-- expected/
|   +-- snapshots/
+-- test_*.py
+-- test_integration.py
```

Notes:
- `core/` must be pure: no file I/O, no network, no timestamps.
- CLI must be thin: argument parsing, I/O, error formatting, and exit codes only.

---

## Data flow (locked, with specific libraries)

Pipeline order is mandatory (security and correctness):

```
HTML string (user input)
  -> nh3.clean()                    [core/sanitizer.py]
  -> BeautifulSoup(..., "lxml")     [core/parser.py]
  -> select main content subtree    [core/content_selector.py]
  -> parse to internal model        [core/parser.py + core/degradation.py]
  -> render self-contained HTML     [core/renderer.py + core/constants.py]
  -> HTML string (output)
```

Important:
- Sanitization occurs before parsing and before content selection.
- The sanitizer allowlist must include `main`, `article`, and `body`, otherwise content selection can break.

---

## Testing strategy (locked)

Required test layers:

1) Golden file tests (end-to-end)
- input HTML fixture -> expected output HTML fixture
- byte-for-byte comparison

2) Model snapshot tests (parser-only)
- DOM -> Internal Document Model -> JSON
- compare against stored snapshots

3) Determinism test
- run conversion twice with identical input/version/flags
- outputs must be byte-identical

Fixture corpus:
- Minimum set is defined in [decisions.md](decisions.md) (real-world HTML, not hand-crafted micro HTML).

---

## Deferred to v2 (explicit)

Out of scope for v1 (do not implement in v1):

- Additional CLI commands:
  - `validate`
  - `info`
  - `--report json`
- Additional fonts beyond OpenDyslexic
- Native PDF generation (v1 uses browser print-to-PDF)
- Additional input formats (PDF, DOCX, Markdown)
- Heuristic readability extraction or scraping-style algorithms
