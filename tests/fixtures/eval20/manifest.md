# Eval20 Fixture Manifest

Evaluation set for Flowdoc Viability Plan (docs/viability-plan.md).
Fixed set — do not change filenames or scoring criteria mid-run.

| # | filename | source_url | capture_date | scope | notes |
|---|----------|------------|--------------|-------|-------|
| 01 | aeon.html | https://aeon.co/essays/how-the-harsh-icy-world-of-snowball-earth-shaped-life-today | UNKNOWN (existing fixture) | in-scope | Long-form essay. Known: 6x [Form omitted] placeholder run at tail. |
| 02 | cdc.html | https://www.cdc.gov/west-nile-virus/symptoms-diagnosis-treatment/index.html | UNKNOWN (existing fixture) | in-scope | Government health article. |
| 03 | eater.html | https://www.eater.com/dining-out/919418/lisbon-pastel-de-nata-tourism-gentrification-portugal | UNKNOWN (existing fixture) | in-scope | Food/restaurant article. Known: consecutive image placeholder runs. |
| 04 | guardian.html | https://www.theguardian.com/food/2020/feb/13/how-ultra-processed-food-took-over-your-shopping-basket-brazil-carlos-monteiro | UNKNOWN (existing fixture) | in-scope | News article. Known: Trafilatura extracts navigation; fails in extract mode (ValidationError). |
| 05 | nhs.html | https://www.nhs.uk/conditions/dyslexia/ | UNKNOWN (existing fixture) | in-scope | UK health service article. |
| 06 | pbs.html | https://www.pbs.org/newshour/arts/explainer-here-is-why-crowd-surges-can-kill-people | UNKNOWN (existing fixture) | in-scope | Public broadcasting article. |
| 07 | propublica.html | https://www.propublica.org/article/3m-forever-chemicals-pfas-pfos-inside-story | UNKNOWN (existing fixture) | in-scope | Investigative journalism article. Known: consecutive [Form omitted] run. |
| 08 | skysports.html | https://www.skysports.com/football/news/11095/13511444/home-advantage-is-on-the-wane-in-the-premier-league-between-the-lines | UNKNOWN (existing fixture) | in-scope | Sports news article. |
| 09 | smithsonian.html | https://www.smithsonianmag.com/science-nature/essential-timeline-understanding-evolution-homo-sapiens-180976807/ | UNKNOWN (existing fixture) | in-scope | Magazine article. Clean extraction reference fixture. |
| 10 | theringer.html | https://www.theringer.com/2024/07/25/olympics/chase-budinger-paris-2024-olympics-beach-volleyball | UNKNOWN (existing fixture) | in-scope | Entertainment/sports article. Known: Trafilatura extracts navigation stub; fails in extract mode (ValidationError). |
| 11 | wikipedia-gdp-table.html | https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal) | 2026-02-28 | out-of-scope | Reference/table page: GDP data tables with no article prose. |
| 12 | w3c-validator-tool.html | https://validator.w3.org/ | 2026-02-28 | out-of-scope | Tool/form interface: HTML validation service, no article content. |
| 13 | article-13-theconversation.html | https://theconversation.com/will-ai-accelerate-or-undermine-the-way-humans-have-always-innovated-272246 | 2026-02-28 | in-scope | Academic long-form prose: AI and human innovation, ~1400 words. |
| 14 | article-14-sciencedaily.html | https://www.sciencedaily.com/releases/2025/11/251130050712.htm | 2026-02-28 | in-scope | Science journalism prose: memory formation neuroscience, ~950 words. |
| 15 | article-15-quantamagazine.html | https://www.quantamagazine.org/how-smell-guides-our-inner-world-20250703/ | 2026-02-28 | in-scope | Long-form feature journalism: olfaction and neuroscience, ~3500 words. |
| 16 | article-16-e360yale.html | https://e360.yale.edu/features/cape-town-baboons | 2026-02-28 | in-scope | Environmental feature journalism: baboon-human coexistence in Cape Town, ~2345 words. |
| 17 | article-17-hakaimagazine.html | https://hakaimagazine.com/features/caviar-pizzas-new-money-and-the-death-of-an-ancient-fish/ | 2026-02-28 | in-scope | Long-form narrative journalism: sturgeon fishing, caviar economy, ~4952 words. |
| 18 | article-18-undark.html | https://undark.org/2026/02/26/brain-organoids-big-questions/ | 2026-02-28 | in-scope | Science journalism: brain organoid research ethics and complexity, ~3773 words. |
| 19 | article-19-insideclimate.html | https://insideclimatenews.org/news/26022026/us-government-accelerates-pacific-coral-reef-collapse/ | 2026-02-28 | in-scope | Investigative science journalism: coral reef collapse and federal policy, ~1729 words. |
| 20 | article-20-sciencefriday.html | https://www.sciencefriday.com/articles/miyawaki-miniforest-rewilding/ | 2026-02-28 | in-scope | Science feature: Miyawaki miniforest rewilding movement, ~1581 words. |

## Planned composition for rows 11–20

Per viability-plan.md V1:
- 2 "out of scope" pages — tables/reference/interactive (rows 11–12, added first)
- 6 "likely in-scope" semantic prose articles from diverse sources (rows 13–18)
- 2 "hard but plausible" CMS-heavy prose pages (rows 19–20)
