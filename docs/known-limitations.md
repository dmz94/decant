# Flowdoc v1 - Known Limitations

**Status:** Reference document for v2 planning
**Last updated:** February 25, 2026
Architecture terminology follows docs/architecture.md and docs/decisions.md.

Known limitations identified during visual validation of the conversion pipeline. These are not bugs - they are documented boundaries of v1 scope.

---

## Trafilatura Extraction Limitations

These affect Trafilatura-based extraction in the conversion pipeline.

**Trailing CMS boilerplate** - Some sites (Cleveland Clinic, WikiHow) have
CMS footer patterns that Trafilatura does not strip. Legitimate article content
is intact but followed by footer noise. Too site-specific to fix generally in v1.

**Inline code promoted to pre blocks** - Trafilatura promotes inline code tags
to block-level pre in some cases, fragmenting surrounding sentences. Not fixable
without risky heuristics.

**Missing spaces around inline elements** - Trafilatura drops spaces at some
inline element boundaries. Not fixable without fragile regex post-processing.

**Duplicate list items** - Trafilatura flattens some nested lists incorrectly,
emitting items twice. Deduplication risks dropping legitimately repeated content.

**Wikipedia lead section fragmentation** - Dense link-heavy paragraphs fragment
into single-phrase paragraphs. Atypical structure. Defer to v2.

---

## Scope Boundaries

**MDN reference table pages** - Content lives in tables which Flowdoc strips.
Wrong input type - Flowdoc is for prose articles, not reference tables.

**Recipe sites** - Trafilatura strips heading structure from some recipe sites
causing validation failure. Out of scope for v1.

**Yale regression (fixed)** - Synthetic H1 injection duplicated the first
real heading, causing drop_duplicate_consecutive_sections() to delete the
definition section. Fixed in Phase 2 by adding a normalization guard that
skips injection when the title matches the first extracted heading.

---

## Deferred to v2

**Italic/em rendering** - Revisit if real-world testing surfaces issues with
italic overuse in specific document types.

**Wikipedia dense link fragmentation** - Needs smarter paragraph merging logic.

**Trailing boilerplate** - Needs site-specific rules or ML-based extraction.
