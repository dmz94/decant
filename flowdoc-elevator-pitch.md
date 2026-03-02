# Flowdoc - Elevator Pitch

## What It Is

A free, open-source command-line tool that converts web articles into
clean, accessible, self-contained HTML files styled for readers with
dyslexia and related conditions.

## The Problem

A parent gets their child's dyslexia diagnosis. They search NHS, BDA,
Understood.org. The content is there but it is buried in site chrome,
cramped typography, and layouts designed for sighted neurotypical readers.
Browser Reader Mode helps but it is ephemeral -- you cannot save it
reliably, print it with controlled typography, email it to a teacher,
or hand it to a student on a USB stick.

Teachers, SEN coordinators, and parents need actual documents: portable,
printable, readable offline, with typography tuned for accessibility.
Today that means manual reformatting. Flowdoc automates it.

## What It Does

Give it an HTML article. It strips the chrome, extracts the content,
and produces a single self-contained HTML file with:
- BDA-recommended sans-serif typography
- Controlled line length, spacing, and contrast
- No external dependencies (works offline, prints cleanly)
- Optional OpenDyslexic font toggle

One command. One file out. Works on NHS, BBC Bitesize, Guardian,
IDA, and similar prose-article sites.

## Who It Is For

- Parents preparing reading materials for dyslexic children
- SEN coordinators and teachers creating accessible handouts
- Accessibility practitioners who need portable document conversion
- Tutors preparing session materials from web content

## Current State

Core pipeline built and tested. Recent evaluation against 11
real-world fixtures: 8 clean passes, 1 marginal, 2 failures
(both are known limitations with dense Wikipedia content).
The tool works well on the sites this audience actually uses.

## Effort to Ship v1

Estimated remaining work for a usable open-source release:
- OpenDyslexic font embedding (spec'd, not yet implemented)
- Input validation polish (largely done)
- CLI packaging for pip install (config exists)
- README and basic usage docs (partially done)
- 2-4 weeks of part-time effort

## What It Is Not

- Not a business. Not a platform. Not a SaaS product.
- Not a browser extension or consumer app.
- Not a Reader Mode replacement (it is a document preparation tool).
- Not a universal web converter (it works on prose articles with
  semantic HTML; non-article content is rejected cleanly).

## Why It Might Matter

10% of the population has some degree of dyslexia. Every one of
them has a parent, a teacher, or a practitioner who has manually
reformatted a document at some point. If Flowdoc saves even a
fraction of that effort and produces a better result, it justifies
existing as a small, focused, free tool.
