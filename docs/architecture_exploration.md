
No hidden state. No project files. No persistent configuration. No embedded application logic.

This implies:

- Deterministic output.
- Clear exit codes.
- Errors to stderr.
- Output to stdout (or explicit file).
- Safe for scripting and piping.
- Predictable behavior in automation contexts.

If the engine is cleanly separated from the CLI, the CLI can remain thin and composable. That keeps scope tight and avoids it turning into an application platform.

The danger to watch is feature creep — adding flags or behaviors that shift it from “transformer” to “application.” That boundary matters.

---

## 3) Does CLI-first make this hard for non-technical users?

That concern is valid.

A CLI-first tool inherently limits accessibility for non-technical users. However, sequencing matters.

If you build a wrapper too early, you multiply surface area:
- UI decisions
- Packaging decisions
- Preview logic
- Platform quirks
- Distribution complexity

Before the engine is validated, that’s risk.

The better sequence is:

1. Build the engine.
2. Expose it via CLI.
3. Validate value with real users.
4. Add a minimal wrapper if and when it’s justified.

The wrapper is packaging, not architecture. If the engine is cleanly separated (library-first), adding a drag-and-drop wrapper later becomes straightforward.

The architectural priority now is separation of concerns — not user interface.

---

## 4) I want other developers to be able to incorporate this into their tools.

This is an important strategic point.

If Flowdoc is to be embedded in something like a recipe manager, the architecture must support it from day one.

That implies:

- A clean internal model.
- Deterministic transformation.
- No reliance on raw DOM structures in rendering.
- A stable engine boundary.
- Library-first design, CLI as a thin layer.

There are two possible integration surfaces:

1. Direct library import.
2. CLI invocation with predictable contract.

Library-first architecture is significantly more attractive for real integration. If the core logic is separable and clean, integration becomes feasible. If everything is wired through CLI assumptions, it becomes harder.

Even if integration isn’t immediate, designing for it now prevents painful refactoring later.

---

## 5) Long-term roadmap: wrapper? browser extension? library? what else?

Several expansion paths exist:

- Desktop wrapper
- Local web UI
- Browser extension
- Additional input formats (Markdown, DOCX)
- Native PDF generation

The risk is expanding before validating the core transformation.

The disciplined sequence should be:

- Engine first.
- Validate with dyslexic readers.
- Stabilize transformation rules.
- Expand only if justified.

A browser extension, for example, pushes the project toward scraping and heuristic extraction. That’s a different problem space.

A wrapper is packaging. It should not dictate engine design.

The architecture should assume expansion is possible — but not necessary for v1.

---

## 6) Parsing HTML is well understood. Shouldn’t we reuse libraries?

Yes. Absolutely.

HTML parsing and sanitization are solved problems. Flowdoc should not implement its own parser.

The pipeline should look like:

HTML → parsed DOM (library) → internal model → renderer → output HTML

Flowdoc’s value is in:

- The internal document model.
- Deterministic degradation rules.
- Readability-focused rendering.
- Typography and layout decisions.

Not in reinventing HTML tokenization or security sanitization.

It is also important to draw a boundary:

- Content selection should remain deterministic (main → article → body).
- No heuristic readability algorithms in v1.
- No scraping-style content guessing.

Otherwise the project shifts scope entirely.

---

## 7) Anything else to consider?

A few structural considerations surfaced during discussion:

- Determinism should include version and flag context.
- Golden-file tests will likely be necessary to prevent formatting drift.
- Renderer must not depend on DOM shortcuts.
- Engine and interface must remain separate.
- Embedded font size implications should be understood.
- Scope creep is the main long-term risk.

None of these change the immediate next step, but they shape how Step 4 and Step 5 should be implemented.

---

This captures the current architectural thinking before implementation begins.
