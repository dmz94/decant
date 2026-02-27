# Flowdoc Strategy (Canonical)

Status: Active  
Supersedes: prior exploratory and session summary documents  
Last Updated: 2026-02-27  

This document defines the canonical identity, scope, and direction of Flowdoc.
If any other document conflicts with this one, this document wins.

---

# Flowdoc - Strategic Positioning (Revised)
## An Accessibility Document Compiler for Prose Content

Version: Strategy Draft v2
Status: For structured review and critique

---

## 1. Core Identity

Flowdoc is an accessibility-focused document compiler for prose content.

It transforms semantic HTML into portable, self-contained, readable artifacts
using a deterministic, security-bounded transformation pipeline.

Flowdoc is not:
- A browser reader mode replacement
- A layout-preserving renderer
- A universal web restructuring engine
- A consumer-first reading app

It is infrastructure that enables institutions to reliably produce accessible
reading versions of prose documents at scale.

---

## 2. Problem Definition

Organizations publish large volumes of prose content:
- Educational articles
- Health information
- Knowledge base content
- Encyclopedic entries
- Editorial/blog content

Producing accessible versions of this content today is often:
- Manual
- Inconsistent
- Not reproducible
- Not portable
- Not suitable for CI or audit

Browser Reader Mode improves readability, but:
- Does not generate portable artifacts
- Cannot run server-side
- Cannot guarantee deterministic output
- Cannot be version-pinned
- Cannot be integrated into institutional workflows

There is no deterministic, embeddable, reproducible transformation engine
designed specifically for accessibility-first document normalization.

---

## 3. System Architecture (Conceptual)

Flowdoc behaves like a compiler:

Input: Semantic HTML (prose)
    -> Main content extraction
    -> Sanitization (security boundary)
    -> Parse into explicit internal model (IR)
    -> Deterministic structural transformation and degradation
    -> Render to self-contained accessible HTML

Key properties:

- Deterministic: same input + version + flags = byte-identical output
- Self-contained: single HTML file, no external dependencies
- Security-bounded: strict sanitization before parsing
- Model-driven: renderer consumes IR only (no raw DOM)
- Fail-fast: non-semantic inputs are rejected explicitly
- Version-pinned: dependency changes are intentional events

This makes Flowdoc suitable for CI pipelines, compliance workflows,
publishing systems, and archival environments.

---

## 4. v1 Scope (Intentionally Narrow)

Supported inputs:
- Article-like prose documents
- Structured via h1-h3 and p/ul/ol
- Server-rendered semantic HTML only

Explicit exclusions:
- JavaScript-rendered SPAs
- Table-heavy reference content
- Forms and interactive applications
- Layout fidelity preservation
- PDF/DOCX input
- GUI or hosted SaaS

Flowdoc rejects non-semantic HTML rather than guessing.

This constraint preserves determinism and clarity.

---

## 5. Accessibility Focus

Initial focus: dyslexia-informed readability principles.

Includes:
- Sans-serif typography
- Controlled line length
- Increased spacing
- High-contrast palette
- No full justification
- Print-friendly formatting
- Portable offline artifact

Flowdoc does not claim universal efficacy.
Validation must be empirical.

---

## 6. Differentiation

Flowdoc differs from browser reader modes by providing:

1. Portable artifact output
2. Deterministic, reproducible results
3. Server-side embeddable engine
4. Explicit degradation contracts
5. Security-bounded transformation
6. Version-pinned stability

It differs from accessibility overlays by transforming structure,
not merely applying CSS.

---

## 7. Intended Adoption Model

End beneficiaries:
Readers who benefit from improved readability (initially dyslexic readers).

Primary adopters:
- Educational institutions
- Learning platforms
- Publishers
- Enterprise knowledge systems
- Accessibility compliance teams
- Archival and documentation systems

Flowdoc is infrastructure with human impact.

---

## 8. User-Facing Surface (Validation Layer)

Although Flowdoc is infrastructure-first, a minimal user-facing tool is
necessary for:

- Demonstrating output quality
- Supporting empirical validation
- Enabling side-by-side comparison
- Allowing artifact download and print testing

This user-facing surface is not the product identity.
It is a validation and demonstration interface.

It may be:
- A minimal local preview web app
- A simple upload-and-convert demo tool

It must not compromise:
- Input constraints
- Determinism
- Security boundary

---

## 9. Quality Model

Flowdoc follows a compiler-style quality model:

- Deterministic output
- Explicit internal representation
- Structured degradation rules
- Stable contracts
- Golden test corpus
- Dependency pinning

Future improvements resemble compiler passes:
- Paragraph repair
- Boilerplate trimming
- Structural normalization
- Fragment merging
- Nested list correction

Expansion deepens prose quality before broadening scope.

---

## 10. Known Limitations (v1)

- Dependent on extraction engine behavior
- CMS boilerplate may leak
- Dense link-heavy pages may fragment
- Table-heavy reference pages rejected intentionally
- No JS-rendered page support

These are documented boundaries, not defects.

---

## 11. Validation Plan

Before expansion:

1. Structured testing with diagnosed dyslexic readers
2. Compare:
   - Original formatting
   - Browser Reader Mode
   - Flowdoc output
3. Measure:
   - Reread frequency
   - Line-loss incidents
   - Subjective fatigue
   - Preference and print usability

If no meaningful benefit is demonstrated,
scope expansion is premature.

---

## 12. Strategic Expansion Path

Phase 2:
- Improve extraction repair quality
- Increase tolerance for imperfect semantic HTML

Phase 3:
- Additional accessibility profiles (ADHD, low vision, etc.)
- Additional delivery surfaces (hosted or extension)

Phase 4:
- Optional additional input front-ends (PDF/DOCX) if IR stability remains intact

All expansion must preserve:
- Determinism
- Security boundary
- Explicit failure modes

---

## 13. Open Strategic Questions

- Is the prose-document domain large enough to sustain institutional adoption?
- Does deterministic accessibility transformation provide sufficient institutional value?
- What level of extraction imperfection is tolerable?
- Who inside an organization owns this problem?
- Is commercialization open-core, hosted API, or institutional licensing?

---

## 14. Long-Term Identity

Flowdoc aims to be:

An accessibility document compiler for prose content.

It is infrastructure.
It produces durable artifacts.
It reduces remediation effort.
It is auditable and reproducible.
It improves reading outcomes at scale.
