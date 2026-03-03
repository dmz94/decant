# Corpus Expansion Candidates

Status: Triage complete
Created: 2026-03-03
Triage: 2026-03-04

## How to use this file

Each candidate gets annotated during screening:
- KEEP -- passes pipeline, structurally distinct, worth adding
- CUT -- failed fetch, JS-only, paywall, redundant, or out of scope
- BOUNDARY -- useful as a boundary/stress test even if imperfect
- SKIP -- never fetched (bot-blocked, connection error, etc.)

## Candidates

### Cat 1: Education / Dyslexia / Accessibility (target 3-4)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C01 | bda-what-is-dyslexia | https://www.bdadyslexia.org.uk/dyslexia/about-dyslexia/what-is-dyslexia | OK | PASS | CUT | 2s 432w; borderline thin, redundant with other Cat 1 |
| C02 | bda-dyslexia-friendly-training | https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-training | OK | PASS | KEEP | 3s 749w |
| C03 | understood-what-is-dyslexia | https://www.understood.org/en/articles/what-is-dyslexia | OK | PASS | KEEP | 11s 1331w |
| C04 | bbc-bitesize-dyslexia | https://www.bbc.co.uk/bitesize/articles/z6mts4j | OK | PASS | KEEP | 7s 1090w; JS risk cleared |
| C05 | govuk-sen-children | https://www.gov.uk/children-with-special-educational-needs | OK | FAIL | CUT | EXTRACTION_FAIL |

### Cat 2: Health / Medical (target 2-3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C06 | mayoclinic-dyslexia | https://www.mayoclinic.org/diseases-conditions/dyslexia/symptoms-causes/syc-20353552 | OK | PASS | KEEP | 10s 642w |
| C07 | clevelandclinic-dyslexia | https://my.clevelandclinic.org/health/diseases/6005-dyslexia | OK | PASS | KEEP | 1s 1102w |
| C08 | nhs-irlen-syndrome | https://www.nhs.uk/conditions/irlen-syndrome/ | FAILED | SKIP | SKIP | fetch failed |
| C09 | medlineplus-dyslexia | https://medlineplus.gov/dyslexia.html | FAILED | SKIP | SKIP | fetch failed |

### Cat 3: Pittsburgh / Sports (target 3-4)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C10 | profootballhof-steelers | https://www.profootballhof.com/teams/pittsburgh-steelers/team-history/ | OK | PASS | KEEP | 1s 618w |
| C11 | nfl-steelers-history | https://operations.nfl.com/learn-the-game/nfl-basics/team-histories/american-football-conference/north/pittsburgh-steelers/ | OK | FAIL | CUT | VALIDATION_ERROR: tool/form page |
| C12 | bbc-rugby | https://www.bbc.co.uk/sport/rugby-union/articles/c62517gdge0o | FAILED | SKIP | SKIP | fetch failed |
| C13 | worldrugby-beginners | https://www.world.rugby/the-game/beginners-guide | OK | PASS | CUT | 3s 205w; too thin |
| C14 | espn-texas-longhorns | https://www.espn.com/college-football/story/_/id/39501205/texas-longhorns-sec-move-everything-know | FAILED | SKIP | SKIP | HIGH JS RISK; fetch failed |
| R01 | espn-jalen-ramsey | https://www.espn.com/espn/feature/story/_/id/24503312/jalen-ramsey-man-mouth-legend | OK | PASS | KEEP | 1s 4666w |

### Cat 4: Texas BBQ / Food (target 2-3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C15 | thc-texas-bbq-history | https://thc.texas.gov/blog/bringing-texas-barbecue-history-table | OK | FAIL | CUT | VALIDATION_ERROR: no headings |
| C16 | texashighways-bbq-culture | https://texashighways.com/food-drink/art-spiritual-pursuit-culture-of-bbq/ | FAILED | SKIP | SKIP | fetch failed |
| C17 | texasmonthly-bbq-history | https://www.texasmonthly.com/bbq/mapping-texas-barbecue-history/ | OK | PASS | KEEP | 1s 630w |
| C18 | sfa-texas-bbq | https://www.southernfoodways.org/oral-history/southern-bbq-trail/texas-bbq/ | OK | PASS | KEEP | 1s 885w |

### Cat 5: Austin / Travel (target 2)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C19 | lonelyplanet-austin | https://www.lonelyplanet.com/articles/best-things-to-do-in-austin | FAILED | SKIP | SKIP | HIGH JS RISK; fetch failed |
| C20 | atlasobscura-austin | https://www.atlasobscura.com/things-to-do/austin-texas | FAILED | SKIP | SKIP | fetch failed |
| C21 | timeout-austin | https://www.timeout.com/austin/things-to-do/best-things-to-do-in-austin | OK | PASS | CUT | 2s 166w; too thin |
| R02 | ricksteves-blog-liverpool | https://blog.ricksteves.com/cameron/2022/01/italy-best-destination-anywhere | OK | PASS | CUT | 1s 2156w; redundant with other Rick Steves picks |
| R03 | ricksteves-blog-mont-blanc | https://blog.ricksteves.com/cameron/ | OK | PASS | KEEP | 11s 3067w |
| R04 | ricksteves-literary-europe | https://www.ricksteves.com/watch-read-listen/read/articles/booking-it-through-literary-europe | OK | PASS | KEEP | 6s 877w |
| R05 | roughguides-barcelona | https://www.roughguides.com/spain/barcelona/ | OK | PASS | KEEP | 63s 8213w |

### Cat 6: Genesis / Peter Gabriel / Music (target 2-3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C22 | britannica-peter-gabriel | https://www.britannica.com/biography/Peter-Gabriel | OK | PASS | CUT | 1s 828w; redundant with better Cat 6 picks |
| C23 | genesis-news-gabriel-bio | https://www.genesis-news.com/article/peter-gabriel-biography/ | OK | PASS | KEEP | 2s 5305w |
| C24 | allaboutjazz-genesis | https://www.allaboutjazz.com/genesis-the-peter-gabriel-years-1967-1975-genesis-by-trevor-maclaren | OK | PASS | KEEP | 2s 1397w |
| C25 | loudersound-gabriel | https://www.loudersound.com/features/peter-gabriel-life-story | OK | PASS | CUT | 1s 6155w; structurally redundant (1 section) |

### Cat 7: Technology / Computers / Unraid (target 2-3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C26 | arstechnica-torvalds | https://arstechnica.com/information-technology/2024/01/linus-torvalds-on-why-he-isnt-mass-mailing-maintainers-to-come-to-his-conference/ | FAILED | SKIP | SKIP | fetch failed |
| C27 | unraid-what-is | https://unraid.net/blog/what-is-unraid | FAILED | SKIP | SKIP | fetch failed |
| C28 | theverge-vision-pro | https://www.theverge.com/2024/1/25/24049050/apple-vision-pro-review | OK | PASS | CUT | 1s 1355w; redundant, Cat 7 well covered |
| C29 | ieee-agi | https://spectrum.ieee.org/what-is-artificial-general-intelligence | FAILED | SKIP | SKIP | fetch failed |
| R06 | berthub-how-tech-loses-out | https://berthub.eu/articles/posts/how-tech-loses-out/ | OK | PASS | CUT | 1s 6100w; redundant, Cat 7 well covered |
| R07 | berthub-long-term-software | https://berthub.eu/articles/posts/on-long-term-software-development/ | OK | PASS | KEEP | 14s 3022w |
| R08 | ieee-spectrum-boeing-max | https://spectrum.ieee.org/how-the-boeing-737-max-disaster-looks-to-a-software-developer | OK | PASS | KEEP | 2s 5785w |
| R09 | ieee-spectrum-unix-history | https://spectrum.ieee.org/the-strange-birth-and-long-life-of-unix | OK | PASS | CUT | 3s 3301w; redundant, Cat 7 well covered |
| R10 | infoq-microservices-ideals | https://www.infoq.com/articles/microservices-design-ideals/ | OK | PASS | CUT | 16s 3517w; redundant, Cat 7 well covered |
| R11 | simonwillison-blog | https://simonwillison.net/2024/Apr/17/ai-for-data-journalism/ | OK | PASS | KEEP | 20s 5672w; transform mode |

### Cat 8: Fitness / Health & Wellness (target 2)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C30 | nhs-couch-to-5k | https://www.nhs.uk/live-well/exercise/running-and-aerobic-exercises/get-running-with-couch-to-5k/ | OK | PASS | KEEP | 18s 1052w |
| C31 | mayoclinic-strength-training | https://www.mayoclinic.org/healthy-lifestyle/fitness/in-depth/strength-training/art-20046670 | OK | PASS | CUT | 5s 913w; redundant, Cat 8 well covered |
| C32 | runnersworld-start-running | https://www.runnersworld.com/training/a20812270/how-to-start-running/ | FAILED | SKIP | SKIP | fetch failed |
| R12 | acefitness-hiit | https://www.acefitness.org/resources/everyone/blog/5483/high-intensity-interval-training-hiit-what-it-is-how-it-works-and-its-benefits/ | OK | FAIL | CUT | VALIDATION_ERROR: nav/ref page |
| R13 | acefitness-strength | https://www.acefitness.org/resources/everyone/blog/5132/the-basics-of-strength-training/ | OK | FAIL | CUT | VALIDATION_ERROR: nav/ref page |
| R14 | harvard-health-4-types-exercise | https://www.health.harvard.edu/exercise-and-fitness/the-4-most-important-types-of-exercise | OK | PASS | CUT | 6s 825w; redundant with other Harvard pick |
| R15 | harvard-health-best-exercises | https://www.health.harvard.edu/staying-healthy/5-of-the-best-exercises-you-can-ever-do | OK | PASS | CUT | 6s 822w; redundant with other Harvard pick |
| R16 | harvard-health-exercise-relax | https://www.health.harvard.edu/staying-healthy/exercising-to-relax | OK | PASS | KEEP | 7s 1675w |
| R17 | medlineplus-exercise | https://medlineplus.gov/howmuchexercisedoineed.html | OK | PASS | CUT | 8s 840w; redundant, Cat 8 well covered |
| R18 | niddk-get-active | https://www.niddk.nih.gov/health-information/weight-management/tips-get-active | OK | PASS | CUT | 3s 193w; too thin |
| R19 | webmd-exercise-benefits | https://www.webmd.com/fitness-exercise/ss/slideshow-7-most-effective-exercises | OK | PASS | CUT | 15s 1082w; redundant, Cat 8 well covered |

### Cat 9: Small / Local / Charity (target 1-2)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C33 | grayshott-history | https://www.grayshotthousing.co.uk/our-history | OK | PASS | KEEP | 3s 997w |
| C34 | grayshott-aims | https://www.grayshotthousing.co.uk/our-aims | OK | PASS | CUT | 13s 442w; borderline thin, redundant with grayshott-history |

### Cat 10: Longform essay / Personal blog (target 2-3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C35 | paulgraham-great-work | https://paulgraham.com/greatwork.html | OK | FAIL | CUT | VALIDATION_ERROR: no headings |
| C36 | joelonsoftware-never-do | https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/ | FAILED | SKIP | SKIP | connection error |
| C37 | danluu-caches | https://danluu.com/simple-hierarchical-caches/ | FAILED | SKIP | SKIP | fetch failed |
| C38 | waitbutwhy-ai | https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html | FAILED | SKIP | SKIP | fetch failed |
| R20 | bearblog-herman | https://herman.bearblog.dev/blog/ | OK | FAIL | CUT | VALIDATION_ERROR: no headings |
| R21 | ribbonfarm-gervais-principle | https://www.ribbonfarm.com/2009/10/07/the-gervais-principle-or-the-office-according-to-the-office/ | OK | PASS | KEEP | 1s 4073w |

### Cat 11: International English news (target 2-3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C39 | abc-australia-music-brain | https://www.abc.net.au/news/science/2024-01-15/how-music-affects-your-brain/103205456 | OK | PASS | KEEP | 6s 1861w |
| C40 | aljazeera-gaza-history | https://www.aljazeera.com/features/2024/1/15/gaza-strip-a-brief-history | FAILED | SKIP | SKIP | fetch failed |
| C41 | bbc-future-dead-sea | https://www.bbc.com/future/article/20240110-how-the-dead-sea-scrolls-were-found | FAILED | SKIP | SKIP | fetch failed |

### Cat 12: Government / Institutional (target 2)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C42 | usagov-disability | https://www.usa.gov/disability-benefits-insurance | STUB | SKIP | SKIP | <1KB stub |
| C43 | nasa-mars-facts | https://www.nasa.gov/solar-system/planets/mars/mars-facts/ | FAILED | SKIP | SKIP | fetch failed |
| C44 | natarchives-magna-carta | https://www.nationalarchives.gov.uk/education/resources/magna-carta/ | OK | PASS | KEEP | 2s 1218w |
| R22 | medlineplus-heart-disease | https://medlineplus.gov/heartdiseases.html | OK | FAIL | CUT | VALIDATION_ERROR: nav/ref page |
| R23 | niddk-diabetes-overview | https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes | OK | PASS | CUT | 10s 1198w; redundant, Cat 12 covered |
| R24 | who-mental-health | https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response | OK | PASS | KEEP | 7s 1005w |

### Cat 13: How-to / Instructional (target 2)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C45 | wikihow-vegetable-garden | https://www.wikihow.com/Start-a-Vegetable-Garden | OK | PASS | KEEP | 9s 2874w |
| C46 | nhs-mindfulness | https://www.nhs.uk/mental-health/self-help/tips-and-support/mindfulness/ | OK | PASS | KEEP | 13s 888w |

### Cat 14: Recipe (origin story, target 3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C47 | homesicktexan-enchiladas | https://www.homesicktexan.com/beef-enchilada-recipe-chili-gravy/ | OK | FAIL | CUT | EXTRACTION_FAIL |
| C48 | whatthefork-cornbread | https://www.whattheforkfoodblog.com/2020/06/28/gluten-free-sourdough-cornbread-recipe/ | OK | PASS | KEEP | 20s 1317w |
| C49 | bakedcollective-muffins | https://bakedcollective.com/sourdough-morning-glory-muffins/ | OK | PASS | KEEP | 20s 1109w |

### Cat 15: Boundary probes (target 2)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C50 | wikipedia-dyslexia | https://en.wikipedia.org/wiki/Dyslexia | OK | PASS | KEEP | 24s 5823w |
| C51 | nhs-dyslexia-diagnosis | https://www.nhs.uk/conditions/dyslexia/diagnosis/ | OK | PASS | CUT | 6s 711w; redundant, boundary probes covered |
| C52 | pmc-dyslexia-research | https://pmc.ncbi.nlm.nih.gov/articles/PMC7455053/ | FAILED | SKIP | SKIP | fetch failed |
| R25 | plos-one-open-access | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270268 | OK | PASS | KEEP | 55s 22849w |

### Cat 16: IRS / HMRC / Gov benefits (target 2-3)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C53 | irs-earned-income-credit | https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit-eitc | OK | FAIL | CUT | VALIDATION_ERROR: nav/ref page |
| C54 | irs-child-tax-credit | https://www.irs.gov/credits-deductions/individuals/child-tax-credit | OK | PASS | KEEP | 11s 756w |
| C55 | hmrc-self-assessment | https://www.gov.uk/self-assessment-tax-returns | OK | PASS | CUT | 5s 297w; too thin |
| C56 | govuk-pip | https://www.gov.uk/pip | OK | PASS | KEEP | 11s 560w |

### Cat 17: Modern publishing platforms (target 3-4)

| ID  | Slug | URL | Fetch | Pipeline | Verdict | Notes |
| --- | ---- | --- | ----- | -------- | ------- | ----- |
| C57 | substack-dyslexia-myths | https://readwritejen.substack.com/p/why-dyslexia-myths-persist | OK | PASS | KEEP | 12s 2719w |
| C58 | substack-dyslexia-advocacy | https://carolsdyslexicadvocacy.substack.com/p/dyslexia-dysgraphia-dyspraxia-and | OK | PASS | CUT | 8s 1465w; redundant with substack-dyslexia-myths |
| C59 | medium-dyslexia-parenting | https://medium.com/inspired-ideas-prek-12/what-parents-need-to-know-about-dyslexia-1a477c25d2d4 | FAILED | SKIP | SKIP | JS RISK confirmed; fetch failed |
| C60 | ghost-accessibility-blog | https://www.marcozehe.de/my-journey-to-ghost/ | OK | PASS | KEEP | 10s 2033w |
| R26 | berthub-cloud-overview | https://berthub.eu/articles/posts/cloud-overview/ | OK | PASS | CUT | 28s 3023w; redundant, Cat 17 well covered |
| R27 | buttondown-blog-email-template | https://buttondown.com/blog/2023-11-02 | OK | PASS | CUT | 1s 364w; too thin |
| R28 | devto-longform | https://dev.to/t/essay | OK | FAIL | CUT | EXTRACTION_FAIL |
| R29 | mataroa-nutcroft-blog | https://nutcroft.mataroa.blog/blog/the-ideal-blog-platform/ | OK | PASS | KEEP | 3s 639w; transform mode |
