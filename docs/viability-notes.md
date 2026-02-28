# Viability V3 - Baseline eval20 run (no code changes)

Run date: 2026-02-28. Flowdoc production default (baseline extraction mode).
17 of 20 fixtures ACCEPT; 3 REJECT. All 3 rejects are in-scope fixtures.
Both out-of-scope fixtures (wikipedia table, w3c tool) produced ACCEPT — they were not rejected cleanly; noted as a known gap.

| # | fixture | expected_scope | status | reason | chars | paragraphs |
|---|---------|---------------|--------|--------|------:|----------:|
| 01 | aeon | in-scope | ACCEPT | OK | 26445 | 65 |
| 02 | cdc | in-scope | ACCEPT | OK | 6357 | 39 |
| 03 | eater | in-scope | ACCEPT | OK | 21661 | 91 |
| 04 | guardian | in-scope | REJECT | No article body detected (nav/boilerplate extracted) | 178 | 0 |
| 05 | nhs | in-scope | ACCEPT | OK | 6854 | 48 |
| 06 | pbs | in-scope | ACCEPT | OK | 9581 | 51 |
| 07 | propublica | in-scope | ACCEPT | OK | 55301 | 124 |
| 08 | skysports | in-scope | ACCEPT | OK | 6988 | 43 |
| 09 | smithsonian | in-scope | ACCEPT | OK | 19304 | 60 |
| 10 | theringer | in-scope | REJECT | No article body detected (nav/boilerplate extracted) | 178 | 0 |
| 11 | wikipedia-gdp-table | out-of-scope | ACCEPT | OK | 6665 | 30 |
| 12 | w3c-validator-tool | out-of-scope | ACCEPT | OK | 4044 | 31 |
| 13 | article-13-theconversation | in-scope | ACCEPT | OK | 11068 | 38 |
| 14 | article-14-sciencedaily | in-scope | ACCEPT | OK | 12036 | 68 |
| 15 | article-15-quantamagazine | in-scope | ACCEPT | OK | 24032 | 75 |
| 16 | article-16-e360yale | in-scope | REJECT | Lacks semantic structure (no h1–h3 + body content) | 95 | 0 |
| 17 | article-17-hakaimagazine | in-scope | ACCEPT | OK | 31282 | 82 |
| 18 | article-18-undark | in-scope | ACCEPT | OK | 33354 | 122 |
| 19 | article-19-insideclimate | in-scope | ACCEPT | OK | 7366 | 39 |
| 20 | article-20-sciencefriday | in-scope | ACCEPT | OK | 2616 | 23 |

## Reject details (full error text)

**04 guardian / 10 theringer:**
> No article body detected: document contains no paragraph with 20 or more words of prose text. Extraction may have captured navigation or boilerplate instead of article content.

**16 article-16-e360yale:**
> Input HTML lacks semantic structure (requires at least one h1-h3 and body content in p/ul/ol).
