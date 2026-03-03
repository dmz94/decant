# Flowdoc - Project Rules for Claude Code

## Identity

Flowdoc is a free, open-source CLI tool that converts semantic HTML into
accessible, self-contained, printable HTML documents for readers with
dyslexia and related conditions.

It is a focused utility for parents, teachers, SEN coordinators, and
accessibility practitioners. Not infrastructure. Not a platform. Not a
business. Not a consumer app.

Primary users are developers and technical practitioners. Parents and
teachers are reached through surfaces built on the engine.

## v1 Scope (Non-Negotiable)

Inputs:
- Server-rendered semantic HTML
- Article-like prose structure

Explicit Non-Goals:
- No JavaScript execution
- No SPA rendering
- No URL fetching
- No dynamic DOM evaluation
- No universal web support

Fail fast on unsupported input.
Do not silently guess.

## Engineering Constraints

- Deterministic output:
  Same input + version + flags -> byte-identical output.

- Security boundary:
  Always sanitize before parsing.
  Never trust raw HTML.

- Structured architecture:
  Maintain IR/model layer.
  Renderer must not consume raw DOM.

- Small changes:
  Implement the smallest change that satisfies the task.
  Do not refactor broadly without explicit instruction.

## Work Process Rules

- When behavior changes, update or extend tests and fixtures.
- If a requested change expands scope, stop and ask.
- Do not introduce new features unless explicitly requested.
- Keep strategy, scope, and decisions aligned.
