# Benchmark Structural Audit

Structural analysis of the ScrapingHub (181 pages) and WCEB (3,985 pages)
benchmark corpora. Complements the pass/fail data in benchmark-results.md
with detailed element-level analysis.

## Table Survey (2026-03-10)

Scanned all 4,166 benchmark HTML files for table characteristics.

### Frequency

| Metric | ScrapingHub (181) | WCEB (3,985) | Combined (4,166) |
|---|---:|---:|---:|
| Files with tables | 13 (7%) | 1,848 (46%) | 1,861 (45%) |
| Total top-level tables | 42 | 5,906 | 5,948 |

### Size distribution

| Size | Count | Percentage |
|---|---:|---:|
| <= 5 rows | 4,455 | 75% |
| 6-10 rows | 597 | 10% |
| > 10 rows | 896 | 15% |

### Complexity

| Feature | Count | Percentage |
|---|---:|---:|
| With colspan | 1,762 | 30% |
| With rowspan | 477 | 8% |
| With nested tables | 1,666 | 28% |

### Layout tables

| Pattern | Count | Percentage |
|---|---:|---:|
| 1x1 layout wrappers | 871 | 15% |
| 1x1 with prose (>= 20 words) | 83 | 1.4% |

The 83 prose-trapping layout tables are almost entirely from old WCEB
pages (early 2000s table-based layouts). ScrapingHub (modern curated
articles) has zero.

### Simple table candidates

2,405 tables (40%) qualify as simple: <= 10 rows, no colspan, no
rowspan, no nested tables, more than 1 cell. These are renderable
in v1.

### Decisions informed

- Layout table unwrapping deferred to v2. Only 2% of files affected,
  concentrated in pre-HTML5 pages outside Flowdoc's target.
- Simple table rendering confirmed as high-value v1 work. 40% of all
  tables in the wild are candidates.

## Comprehensive Structural Audit

Pending. Will cover: image preservation, heading hierarchy, list
nesting, definition lists, paragraph distribution, placeholder density.
Script: tests/benchmark-structural/run_structural_audit.py
