# Flowdoc - Project Rules for Claude Code

## Identity

Flowdoc is an accessibility document compiler for prose content.

It transforms semantic, server-rendered HTML prose into a self-contained,
portable, accessible HTML artifact.

This is infrastructure-first software.
It is not a general-purpose browser reader.
It is not a hosted service.
It is not a consumer app.

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
