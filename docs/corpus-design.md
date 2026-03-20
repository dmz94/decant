# Decant Corpus Design

## Purpose

This document defines the category framework and coverage targets
for the Decant regression test corpus. Target: 100 fixtures.

Decant works best on pages written mainly to be read top to bottom:
articles, blog posts, and clear information pages. The corpus should
reflect the kinds of pages real users actually want to convert.

## Categories (16)

Categories reflect three realities:

1. What people actually go looking for online
2. What kinds of pages they genuinely want to read top to bottom
3. What page structures are distinctive enough to expose regressions

1. News and reported articles
2. Long-form features
3. Opinion and essays
4. Health and medical information
5. Education and learning resources
6. Recipes and cooking
7. How-to and practical advice
8. Government, official, and institutional guidance
9. Science, nature, and environment
10. History, reference, and general explainers
11. Wikipedia and reference-style pages
12. FAQ and help-center guidance
13. Editorial reviews and recommendations
14. Travel and culture
15. Sports writing
16. Academic and evidence summaries

### Tracked in notes, not as categories

- SEN / parent / child-development relevance
- Nonprofit / advocacy source
- Paywalled or metered content
- Structural flags: comparison-heavy, table-heavy, listicle,
  citation-heavy, FAQ/accordion, recipe
- Fit level: strong fit, borderline, known bad fit
- Local/small website (simple CMS, idiosyncratic HTML)

## Classification Rules

Classify each fixture by its primary reading intent, not just
subject matter. One primary bucket per fixture. Use the notes
column for secondary traits.

### Boundary cases

**How-to vs FAQ/help-center.** Use how-to when the page is a
guided sequence or practical advice written as continuous prose.
Use FAQ/help-center when the page is organized as short Q&A pairs,
support-style sections, or accordion content.

**History/reference/explainers vs Wikipedia/reference-style.** Use
Wikipedia/reference-style when the page comes from a reference
platform with encyclopedia-like structure: TOC, infobox, citation
apparatus, entry-like organization. Use history/reference/explainers
for other non-science background reading that is prose-led but not
platform-reference style.

**Education vs Government/institutional.** Use education when the
page is primarily teaching or learning content. Use
government/institutional when the page is official policy,
administrative guidance, or procedural information from an
institution.

**News vs Long-form vs Opinion.** Use news for reported articles
primarily conveying events or facts. Use long-form for narrative,
feature-like pieces materially longer and more structured than a
standard news article. Use opinion for pieces primarily advancing
an argument or personal viewpoint.

**History/reference/explainers -- scope note.** Covers non-science
explanatory and reference reading: history pages, civic/context
explainers, encyclopedia-like entries outside Wikipedia, broad
backgrounders. "General explainers" does not mean "anything
informative that does not fit elsewhere."

**Editorial reviews -- scope note.** Center of the bucket is
prose-led editorial reviews and recommendation articles (e.g.
Wirecutter-style). Include a small number of comparison-heavy
pages as deliberate edge cases. Exclude catalog/comparison
interfaces, product grids, and thin affiliate landing pages.

## Fixture Selection Checklist

Before adding a fixture:

1. Would a real user plausibly want to read this top to bottom?
2. Is it in scope, or mainly a use/browse/interact page?
3. Does it strengthen category coverage or structural coverage?
4. Is it too similar to an existing fixture in layout and failure
   mode?
5. If borderline, is it included deliberately as an edge case?

Each fixture should have a short "why included" note in the
manifest explaining what it tests that other fixtures do not.

When removing a fixture, justify by structural redundancy, not
just topical overlap. Two pages about the same subject may still
be worth keeping if they expose materially different CMS templates,
boilerplate patterns, or content hierarchy.

## Out of Scope

These page types are not good Decant targets:

- Search results pages
- Ecommerce category and product pages
- Live blogs and feeds
- Dashboards and scoreboards
- Interactive tools and calculators
- Forums with fragmented thread structure
- Pure link directories or indexes

## Known Scope Boundaries

These patterns are in scope conceptually but cannot be
handled by the current architecture:

- **JS-loaded accordion/hub pages.** Pages where section
  headers are visible in static HTML but content is fetched
  dynamically on click (e.g. BDA about page at
  bdadyslexia.org.uk/about). The content is not in the
  saved HTML, so there is nothing for the engine to extract.
  Distinct from CSS-hidden accordions (e.g. copyright-gov-faq)
  where content IS in the HTML but collapsed by default --
  those are potential engine fixes.

## Current Fixtures by Category

Fixture counts below are stale (pre-expansion). Update
pending after corpus finalization. The manifest is the
source of truth: tests/pipeline-audit/test-pages/manifest.md

### 1. News and reported articles

| Fixture | Source | Notes |
|---------|--------|-------|
| pbs-crowd-surges.html | pbs.org | Explainer |

### 2. Long-form features

| Fixture | Source | Notes |
|---------|--------|-------|
| propublica-3m-pfas.html | propublica.org | Investigative |
| espn-jalen-ramsey.html | espn.com | Magazine-style sports feature |
| allaboutjazz-genesis.html | allaboutjazz.com | Music retrospective |
| ieee-spectrum-boeing-max.html | spectrum.ieee.org | Technical long-form |

### 3. Opinion and essays

| Fixture | Source | Notes |
|---------|--------|-------|
| theconversation-ai-innovation.html | theconversation.com | Academic op-ed |
| substack-dyslexia-myths.html | substack.com | Newsletter essay |
| ghost-accessibility-blog.html | marcozehe.de | Personal blog |
| ribbonfarm-gervais-principle.html | ribbonfarm.com | Long essay |
| berthub-long-term-software.html | berthub.eu | Tech essay |

### 4. Health and medical information

| Fixture | Source | Notes |
|---------|--------|-------|
| nhs-dyslexia.html | nhs.uk | SEN |
| cdc-west-nile.html | cdc.gov | US government health |
| mayoclinic-dyslexia.html | mayoclinic.org | SEN |
| clevelandclinic-dyslexia.html | clevelandclinic.org | SEN |
| who-mental-health.html | who.int | International health |
| additude-adhd-in-children.html | additudemag.com | SEN, Parent-relevant |
| nhs-couch-to-5k.html | nhs.uk | How-to health |

### 5. Education and learning resources

| Fixture | Source | Notes |
|---------|--------|-------|
| bbc-bitesize-dyslexia.html | bbc.co.uk | SEN |

### 6. Recipes and cooking

| Fixture | Source | Notes |
|---------|--------|-------|
| seriouseats-brisket.html | seriouseats.com | Long-form recipe |

### 7. How-to and practical advice

| Fixture | Source | Notes |
|---------|--------|-------|
| golf-greenside-bunker.html | golf.com | Sports how-to |
| understood-what-is-dyslexia.html | understood.org | SEN, Parent-relevant |
| irs-child-tax-credit.html | irs.gov | Government how-to |

### 8. Government, official, and institutional guidance

| Fixture | Source | Notes |
|---------|--------|-------|
| bda-dyslexia-friendly-training.html | bdadyslexia.org.uk | SEN, Parent-relevant |
| govuk-pip.html | gov.uk | UK government |

### 9. Science, nature, and environment

| Fixture | Source | Notes |
|---------|--------|-------|
| smithsonian-homo-sapiens.html | smithsonianmag.com | Science magazine |
| quanta-smell.html | quantamagazine.org | Science journalism |
| yale360-baboons.html | e360.yale.edu | Environmental feature |
| undark-brain-organoids.html | undark.org | Science journalism |

### 10. History, reference, and general explainers

| Fixture | Source | Notes |
|---------|--------|-------|
| profootballhof-steelers.html | profootballhof.com | Team history page |
| genesis-news-gabriel-bio.html | genesis-news.com | Fan site biography |
| natarchives-magna-carta.html | nationalarchives.gov.uk | Institutional reference |

### 11. Wikipedia and reference-style pages

| Fixture | Source | Notes |
|---------|--------|-------|
| wikipedia-dyslexia.html | wikipedia.org | SEN |

### 12. FAQ and help-center guidance

Empty.

### 13. Editorial reviews and recommendations

Empty.

### 14. Travel and culture

| Fixture | Source | Notes |
|---------|--------|-------|
| texasmonthly-bbq-history.html | texasmonthly.com | Food/culture feature |
| ricksteves-blog-mont-blanc.html | blog.ricksteves.com | Travel blog |
| roughguides-barcelona.html | roughguides.com | Travel guide |

### 15. Sports writing

| Fixture | Source | Notes |
|---------|--------|-------|
| theringer-chase-budinger.html | theringer.com | Sports profile |

### 16. Academic and evidence summaries

| Fixture | Source | Notes |
|---------|--------|-------|
| plos-one-open-access.html | plos.org | Open-access journal article |

### Self-test (outside category system)

| Fixture | Source | Notes |
|---------|--------|-------|
| demo-decanters.html | decant.cc | Decant demo page |

## Coverage Targets

39 current fixtures + 1 self-test. 60 new fixtures needed.

| Category | Have | Target | To add |
|----------|------|--------|--------|
| 1. News and reported articles | 1 | 6 | 5 |
| 2. Long-form features | 4 | 6 | 2 |
| 3. Opinion and essays | 5 | 6 | 1 |
| 4. Health and medical | 7 | 7 | 0 |
| 5. Education and learning | 1 | 6 | 5 |
| 6. Recipes and cooking | 1 | 6 | 5 |
| 7. How-to and practical advice | 3 | 6 | 3 |
| 8. Government and institutional | 2 | 6 | 4 |
| 9. Science, nature, environment | 4 | 6 | 2 |
| 10. History, reference, explainers | 3 | 6 | 3 |
| 11. Wikipedia and reference-style | 1 | 6 | 5 |
| 12. FAQ and help-center | 0 | 6 | 6 |
| 13. Editorial reviews | 0 | 6 | 6 |
| 14. Travel and culture | 3 | 5 | 2 |
| 15. Sports writing | 1 | 5 | 4 |
| 16. Academic and evidence | 1 | 5 | 4 |
| Self-test | 1 | 1 | 0 |
| **Total** | **40** | **100** | **60** |

### Fill priority

1. Empty buckets: FAQ/help-center, editorial reviews
2. Near-empty buckets (1 fixture): news, education, recipes,
   Wikipedia, sports, academic
3. Core audience use cases: SEN-relevant pages across health,
   education, government
4. Structural diversity within covered buckets: different CMS
   templates, failure modes, edge cases

### Coverage requirements

- SEN / parent / child-development: meaningful representation
  across health, education, government, how-to
- Nonprofit / advocacy: representation as source type
- Paywalled / metered: a few fixtures with truncated content
- Local / small website: at least 1-2 fixtures
- Each category should include at least one awkward or adversarial
  fixture, not just clean exemplars
