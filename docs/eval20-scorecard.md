# Eval20 Scorecard

Scoring rubric — 0/1 per criterion:

1. **title** — Title is present in output
2. **intro** — First 1–2 paragraphs of article prose are preserved
3. **no_boilerplate** — No trailing nav/footer/form boilerplate in output
4. **no_artifacts** — No obvious structural artifacts (stray placeholders, broken markup, etc.)
5. **coherent** — Reads as a coherent article on skim

**Clean threshold:** 4/5 or 5/5

Out-of-scope fixtures: mark rubric fields N/A. `accept/reject` = "accept" if Flowdoc rejects cleanly with a clear reason; "reject" if it fails to reject correctly.

---

| index | fixture | expected_scope | title | intro | no_boilerplate | no_artifacts | coherent | total | clean? | accept/reject | reason | notes |
|-------|---------|----------------|-------|-------|----------------|--------------|----------|-------|--------|---------------|--------|-------|
| 01 | aeon.html | in-scope | | | | | | | | | | |
| 02 | cdc.html | in-scope | | | | | | | | | | |
| 03 | eater.html | in-scope | | | | | | | | | | |
| 04 | guardian.html | in-scope | | | | | | | | | | |
| 05 | nhs.html | in-scope | | | | | | | | | | |
| 06 | pbs.html | in-scope | | | | | | | | | | |
| 07 | propublica.html | in-scope | | | | | | | | | | |
| 08 | skysports.html | in-scope | | | | | | | | | | |
| 09 | smithsonian.html | in-scope | | | | | | | | | | |
| 10 | theringer.html | in-scope | | | | | | | | | | |
| 11 | wikipedia-gdp-table.html | out-of-scope | N/A | N/A | N/A | N/A | N/A | N/A | N/A | | | |
| 12 | w3c-validator-tool.html | out-of-scope | N/A | N/A | N/A | N/A | N/A | N/A | N/A | | | |
| 13 | article-13-theconversation.html | in-scope | | | | | | | | | | |
| 14 | article-14-sciencedaily.html | in-scope | | | | | | | | | | |
| 15 | article-15-quantamagazine.html | in-scope | | | | | | | | | | |
| 16 | article-16-e360yale.html | in-scope | | | | | | | | | | |
| 17 | article-17-hakaimagazine.html | in-scope | | | | | | | | | | |
| 18 | article-18-undark.html | in-scope | | | | | | | | | | |
| 19 | article-19-insideclimate.html | in-scope | | | | | | | | | | |
| 20 | article-20-sciencefriday.html | in-scope | | | | | | | | | | |
