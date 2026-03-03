"""
One-time mega-fetch: combine original candidates + 3 rounds of replacements,
deduplicate by URL, fetch everything not already in staging (>2KB).
"""

import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STAGING_DIR = PROJECT_ROOT / "tests" / "fixtures" / "staging"
RESULTS_PATH = Path(__file__).resolve().parent / "mega-fetch-results.txt"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ---- Master URL list: (cat, slug, url) ----
# Original 60 from candidates.md
URLS = [
    # Cat 1: Education / Dyslexia / Accessibility
    (1, "bda-what-is-dyslexia", "https://www.bdadyslexia.org.uk/dyslexia/about-dyslexia/what-is-dyslexia"),
    (1, "bda-dyslexia-friendly-training", "https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-training"),
    (1, "understood-what-is-dyslexia", "https://www.understood.org/en/articles/what-is-dyslexia"),
    (1, "bbc-bitesize-dyslexia", "https://www.bbc.co.uk/bitesize/articles/z6mts4j"),
    (1, "govuk-sen-children", "https://www.gov.uk/children-with-special-educational-needs"),

    # Cat 2: Health / Medical
    (2, "mayoclinic-dyslexia", "https://www.mayoclinic.org/diseases-conditions/dyslexia/symptoms-causes/syc-20353552"),
    (2, "clevelandclinic-dyslexia", "https://my.clevelandclinic.org/health/diseases/6005-dyslexia"),
    (2, "nhs-irlen-syndrome", "https://www.nhs.uk/conditions/irlen-syndrome/"),
    (2, "medlineplus-dyslexia", "https://medlineplus.gov/dyslexia.html"),
    # Round 1 replacements
    (2, "webmd-sleep-benefits", "https://www.webmd.com/sleep-disorders/features/11-surprising-health-benefits-sleep"),
    (2, "healthline-gut-health", "https://www.healthline.com/nutrition/gut-health-tips"),
    (2, "verywell-anxiety-causes", "https://www.verywellmind.com/causes-of-anxiety-2584634"),

    # Cat 3: Pittsburgh / Sports
    (3, "profootballhof-steelers", "https://www.profootballhof.com/teams/pittsburgh-steelers/team-history/"),
    (3, "nfl-steelers-history", "https://operations.nfl.com/learn-the-game/nfl-basics/team-histories/american-football-conference/north/pittsburgh-steelers/"),
    (3, "bbc-rugby", "https://www.bbc.co.uk/sport/rugby-union/articles/c62517gdge0o"),
    (3, "worldrugby-beginners", "https://www.world.rugby/the-game/beginners-guide"),
    (3, "espn-texas-longhorns", "https://www.espn.com/college-football/story/_/id/39501205/texas-longhorns-sec-move-everything-know"),
    # Round 1 replacements
    (3, "espn-jalen-ramsey", "https://www.espn.com/espn/feature/story/_/id/24503312/jalen-ramsey-man-mouth-legend"),
    (3, "smithsonian-baseball", "https://www.smithsonianmag.com/history/the-history-of-baseball-180981505/"),
    (3, "bleacherreport-nba-evo", "https://bleacherreport.com/articles/2940654-the-evolution-of-the-nba"),
    # Round 2 replacements
    (3, "olympics-ioc-history", "https://www.olympics.com/ioc/history"),
    (3, "mentalfloss-sports-names", "https://www.mentalfloss.com/article/57659/where-did-sports-get-their-names"),

    # Cat 4: Texas BBQ / Food
    (4, "thc-texas-bbq-history", "https://thc.texas.gov/blog/bringing-texas-barbecue-history-table"),
    (4, "texashighways-bbq-culture", "https://texashighways.com/food-drink/art-spiritual-pursuit-culture-of-bbq/"),
    (4, "texasmonthly-bbq-history", "https://www.texasmonthly.com/bbq/mapping-texas-barbecue-history/"),
    (4, "sfa-texas-bbq", "https://www.southernfoodways.org/oral-history/southern-bbq-trail/texas-bbq/"),
    # Round 1 replacements
    (4, "smithsonian-food-war", "https://www.smithsonianmag.com/travel/local-cuisine-war-tradition-food-history-cultural-travel-180961610/"),
    (4, "smithsonian-food-humanity", "https://www.smithsonianmag.com/arts-culture/how-food-shaped-humanity-83840262/"),
    # Round 2 replacements
    (4, "atlasobscura-food-marketing", "https://www.atlasobscura.com/articles/american-food-traditions-that-started-as-marketing-ploys"),
    (4, "atlasobscura-food-origins", "https://www.atlasobscura.com/articles/food-origins-map"),
    (4, "mentalfloss-pho-history", "https://www.mentalfloss.com/article/91812/pho-delicious-dish-also-tells-us-lot-about-history-vietnam"),

    # Cat 5: Austin / Travel
    (5, "lonelyplanet-austin", "https://www.lonelyplanet.com/articles/best-things-to-do-in-austin"),
    (5, "atlasobscura-austin", "https://www.atlasobscura.com/things-to-do/austin-texas"),
    (5, "timeout-austin", "https://www.timeout.com/austin/things-to-do/best-things-to-do-in-austin"),
    # Round 1 replacements
    (5, "lonelyplanet-london-westend", "https://www.lonelyplanet.com/articles/3-culture-filled-days-in-londons-west-end"),
    (5, "lonelyplanet-tokyo-guide", "https://www.lonelyplanet.com/articles/first-time-in-tokyo"),
    (5, "frommers-paris", "https://www.frommers.com/destinations/paris/in-depth/history"),
    (5, "roughguides-barcelona", "https://www.roughguides.com/spain/barcelona/"),
    # Round 2 replacements
    (5, "atlasobscura-sun-valley", "https://www.atlasobscura.com/articles/how-sun-valley-idaho-combines-storied-past-vibrant-culture"),
    # Round 3 replacements
    (5, "ricksteves-literary-europe", "https://www.ricksteves.com/watch-read-listen/read/articles/booking-it-through-literary-europe"),
    (5, "ricksteves-blog-liverpool", "https://blog.ricksteves.com/cameron/2022/01/italy-best-destination-anywhere"),
    (5, "ricksteves-blog-mont-blanc", "https://blog.ricksteves.com/cameron/"),

    # Cat 6: Genesis / Peter Gabriel / Music
    (6, "britannica-peter-gabriel", "https://www.britannica.com/biography/Peter-Gabriel"),
    (6, "genesis-news-gabriel-bio", "https://www.genesis-news.com/article/peter-gabriel-biography/"),
    (6, "allaboutjazz-genesis", "https://www.allaboutjazz.com/genesis-the-peter-gabriel-years-1967-1975-genesis-by-trevor-maclaren"),
    (6, "loudersound-gabriel", "https://www.loudersound.com/features/peter-gabriel-life-story"),

    # Cat 7: Technology / Computers / Unraid
    (7, "arstechnica-torvalds", "https://arstechnica.com/information-technology/2024/01/linus-torvalds-on-why-he-isnt-mass-mailing-maintainers-to-come-to-his-conference/"),
    (7, "unraid-what-is", "https://unraid.net/blog/what-is-unraid"),
    (7, "theverge-vision-pro", "https://www.theverge.com/2024/1/25/24049050/apple-vision-pro-review"),
    (7, "ieee-agi", "https://spectrum.ieee.org/what-is-artificial-general-intelligence"),
    # Round 1 replacements
    (7, "acmqueue-concurrency", "https://queue.acm.org/detail.cfm?id=1095421"),
    (7, "acmqueue-developer-prod", "https://queue.acm.org/detail.cfm?id=3454124"),
    (7, "arstechnica-tech-feature", "https://arstechnica.com/science/2024/01/the-physics-of-why-you-cant-make-a-perfect-map/"),
    (7, "wired-tech-feature", "https://www.wired.com/story/chatgpt-openai-artificial-intelligence-future-of-work/"),
    (7, "simonwillison-blog", "https://simonwillison.net/2024/Apr/17/ai-for-data-journalism/"),
    # Round 2 replacements
    (7, "joelonsoftware-unicode", "https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/"),
    (7, "ieee-spectrum-boeing-max", "https://spectrum.ieee.org/how-the-boeing-737-max-disaster-looks-to-a-software-developer"),
    (7, "ieee-spectrum-unix-history", "https://spectrum.ieee.org/the-strange-birth-and-long-life-of-unix"),
    # Round 3 replacements
    (7, "berthub-long-term-software", "https://berthub.eu/articles/posts/on-long-term-software-development/"),
    (7, "berthub-how-tech-loses-out", "https://berthub.eu/articles/posts/how-tech-loses-out/"),
    (7, "infoq-microservices-ideals", "https://www.infoq.com/articles/microservices-design-ideals/"),

    # Cat 8: Fitness / Health & Wellness
    (8, "nhs-couch-to-5k", "https://www.nhs.uk/live-well/exercise/running-and-aerobic-exercises/get-running-with-couch-to-5k/"),
    (8, "mayoclinic-strength-training", "https://www.mayoclinic.org/healthy-lifestyle/fitness/in-depth/strength-training/art-20046670"),
    (8, "runnersworld-start-running", "https://www.runnersworld.com/training/a20812270/how-to-start-running/"),
    # Round 1 replacements
    (8, "webmd-exercise-benefits", "https://www.webmd.com/fitness-exercise/ss/slideshow-7-most-effective-exercises"),
    (8, "acefitness-strength", "https://www.acefitness.org/resources/everyone/blog/5132/the-basics-of-strength-training/"),
    # Round 2 replacements
    (8, "niddk-get-active", "https://www.niddk.nih.gov/health-information/weight-management/tips-get-active"),
    (8, "medlineplus-exercise", "https://medlineplus.gov/howmuchexercisedoineed.html"),
    (8, "acefitness-hiit", "https://www.acefitness.org/resources/everyone/blog/5483/high-intensity-interval-training-hiit-what-it-is-how-it-works-and-its-benefits/"),
    # Round 3 replacements
    (8, "harvard-health-best-exercises", "https://www.health.harvard.edu/staying-healthy/5-of-the-best-exercises-you-can-ever-do"),
    (8, "harvard-health-exercise-relax", "https://www.health.harvard.edu/staying-healthy/exercising-to-relax"),
    (8, "harvard-health-4-types-exercise", "https://www.health.harvard.edu/exercise-and-fitness/the-4-most-important-types-of-exercise"),

    # Cat 9: Small / Local / Charity
    (9, "grayshott-history", "https://www.grayshotthousing.co.uk/our-history"),
    (9, "grayshott-aims", "https://www.grayshotthousing.co.uk/our-aims"),

    # Cat 10: Longform essay / Personal blog
    (10, "paulgraham-great-work", "https://paulgraham.com/greatwork.html"),
    (10, "joelonsoftware-never-do", "https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/"),
    (10, "danluu-caches", "https://danluu.com/simple-hierarchical-caches/"),
    (10, "waitbutwhy-ai", "https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html"),
    # Round 1 replacements
    (10, "aeon-empty-brain", "https://aeon.co/essays/your-brain-does-not-process-information-and-retrieve-memories"),
    (10, "aeon-english-weird", "https://aeon.co/essays/english-is-not-normal"),
    (10, "kottke-longform", "https://kottke.org/24/01/something-interesting"),
    (10, "stratechery-free-post", "https://stratechery.com/2023/an-interview-with-chatgpt/"),
    # Round 2 replacements
    (10, "stratechery-microsoft-reorg", "https://stratechery.com/2013/why-microsofts-reorganization-is-a-bad-idea/"),
    (10, "ribbonfarm-gervais-principle", "https://www.ribbonfarm.com/2009/10/07/the-gervais-principle-or-the-office-according-to-the-office/"),
    (10, "bearblog-herman", "https://herman.bearblog.dev/blog/"),

    # Cat 11: International English news
    (11, "abc-australia-music-brain", "https://www.abc.net.au/news/science/2024-01-15/how-music-affects-your-brain/103205456"),
    (11, "aljazeera-gaza-history", "https://www.aljazeera.com/features/2024/1/15/gaza-strip-a-brief-history"),
    (11, "bbc-future-dead-sea", "https://www.bbc.com/future/article/20240110-how-the-dead-sea-scrolls-were-found"),
    # Round 1 replacements
    (11, "bbc-news-feature", "https://www.bbc.com/news/world-65282905"),
    (11, "guardian-world", "https://www.theguardian.com/world/2024/jan/01/the-world-in-2024-a-year-of-elections"),
    (11, "dw-english-feature", "https://www.dw.com/en/how-germany-is-trying-to-fix-its-broken-economy/a-68149873"),
    (11, "aljazeera-english", "https://www.aljazeera.com/features/2024/1/1/what-to-expect-in-2024"),

    # Cat 12: Government / Institutional
    (12, "usagov-disability", "https://www.usa.gov/disability-benefits-insurance"),
    (12, "nasa-mars-facts", "https://www.nasa.gov/solar-system/planets/mars/mars-facts/"),
    (12, "natarchives-magna-carta", "https://www.nationalarchives.gov.uk/education/resources/magna-carta/"),
    # Round 1 replacements
    (12, "cdc-heart-disease", "https://www.cdc.gov/heartdisease/about.htm"),
    (12, "who-mental-health", "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response"),
    (12, "smithsonian-institution", "https://www.si.edu/about"),
    # Round 2 replacements
    (12, "niddk-diabetes-overview", "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes"),
    (12, "medlineplus-heart-disease", "https://medlineplus.gov/heartdiseases.html"),
    (12, "olympics-ioc-overview", "https://www.olympics.com/ioc/overview"),

    # Cat 13: How-to / Instructional
    (13, "wikihow-vegetable-garden", "https://www.wikihow.com/Start-a-Vegetable-Garden"),
    (13, "nhs-mindfulness", "https://www.nhs.uk/mental-health/self-help/tips-and-support/mindfulness/"),

    # Cat 14: Recipe (origin story)
    (14, "homesicktexan-enchiladas", "https://www.homesicktexan.com/beef-enchilada-recipe-chili-gravy/"),
    (14, "whatthefork-cornbread", "https://www.whattheforkfoodblog.com/2020/06/28/gluten-free-sourdough-cornbread-recipe/"),
    (14, "bakedcollective-muffins", "https://bakedcollective.com/sourdough-morning-glory-muffins/"),

    # Cat 15: Boundary probes
    (15, "wikipedia-dyslexia", "https://en.wikipedia.org/wiki/Dyslexia"),
    (15, "nhs-dyslexia-diagnosis", "https://www.nhs.uk/conditions/dyslexia/diagnosis/"),
    (15, "pmc-dyslexia-research", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7455053/"),
    # Round 1 replacements
    (15, "plos-one-open-access", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270268"),
    (15, "ncbi-pmc-article", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9561544/"),
    # Round 2 replacements (dupes of round 1 — will be deduped)
    (15, "ncbi-pmc-dyslexia", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9561544/"),
    (15, "plos-one-reading", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270268"),
    (15, "ieee-spectrum-max-boundary", "https://spectrum.ieee.org/how-the-boeing-737-max-disaster-looks-to-a-software-developer"),
    # Round 3 replacements
    (15, "iucn-redlist-gorilla", "https://www.iucnredlist.org/species/9404/136250858"),
    (15, "iucn-redlist-tiger", "https://www.iucnredlist.org/species/15955/50659951"),
    (15, "infoq-cell-based-architecture", "https://www.infoq.com/articles/cell-based-architecture-overview/"),

    # Cat 16: IRS / HMRC / Gov benefits
    (16, "irs-earned-income-credit", "https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit-eitc"),
    (16, "irs-child-tax-credit", "https://www.irs.gov/credits-deductions/individuals/child-tax-credit"),
    (16, "hmrc-self-assessment", "https://www.gov.uk/self-assessment-tax-returns"),
    (16, "govuk-pip", "https://www.gov.uk/pip"),

    # Cat 17: Modern publishing platforms
    (17, "substack-dyslexia-myths", "https://readwritejen.substack.com/p/why-dyslexia-myths-persist"),
    (17, "substack-dyslexia-advocacy", "https://carolsdyslexicadvocacy.substack.com/p/dyslexia-dysgraphia-dyspraxia-and"),
    (17, "medium-dyslexia-parenting", "https://medium.com/inspired-ideas-prek-12/what-parents-need-to-know-about-dyslexia-1a477c25d2d4"),
    (17, "ghost-accessibility-blog", "https://www.marcozehe.de/my-journey-to-ghost/"),
    # Round 1 replacements
    (17, "devto-longform", "https://dev.to/t/essay"),
    (17, "hashnode-feature", "https://engineering.hashnode.com/how-hashnode-scaled-to-serve-millions"),
    # Round 2 replacements (some dupes)
    (17, "devto-swyx-essay", "https://dev.to/swyx/the-operating-system-of-you-eog"),
    (17, "bearblog-minimal-cms", "https://herman.bearblog.dev/blog/"),
    (17, "ribbonfarm-platform", "https://www.ribbonfarm.com/2009/10/07/the-gervais-principle-or-the-office-according-to-the-office/"),
    # Round 3 replacements
    (17, "buttondown-blog-email-template", "https://buttondown.com/blog/2023-11-02"),
    (17, "mataroa-nutcroft-blog", "https://nutcroft.mataroa.blog/blog/the-ideal-blog-platform/"),
    (17, "berthub-cloud-overview", "https://berthub.eu/articles/posts/cloud-overview/"),
]


def main():
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    # Deduplicate by URL, keeping first occurrence
    seen_urls = {}
    deduped = []
    dupes_removed = []
    for cat, slug, url in URLS:
        if url in seen_urls:
            dupes_removed.append((cat, slug, url, seen_urls[url]))
            continue
        seen_urls[url] = slug
        deduped.append((cat, slug, url))

    print(f"Total entries: {len(URLS)}")
    print(f"After dedup: {len(deduped)}")
    if dupes_removed:
        print(f"Duplicates removed: {len(dupes_removed)}")
        for cat, slug, url, original_slug in dupes_removed:
            print(f"  Cat {cat:2d} {slug} -> dupe of {original_slug}")
    print()

    # Check which files already exist and are >2KB
    to_fetch = []
    skipped = []
    for cat, slug, url in deduped:
        filepath = STAGING_DIR / f"{slug}.html"
        if filepath.exists() and filepath.stat().st_size > 2048:
            skipped.append((cat, slug, url, filepath.stat().st_size))
        else:
            to_fetch.append((cat, slug, url))

    print(f"Already in staging (>2KB): {len(skipped)}")
    print(f"To fetch: {len(to_fetch)}")
    print()

    session = requests.Session()
    session.headers.update(HEADERS)

    # Fetch
    results = []

    # Record skipped files
    for cat, slug, url, size in skipped:
        results.append({
            "cat": cat, "slug": slug, "url": url,
            "size_kb": size / 1024, "status": "SKIP",
            "http": "-", "reason": "already fetched",
        })

    total_fetch = len(to_fetch)
    for i, (cat, slug, url) in enumerate(to_fetch, 1):
        print(f"  [{i}/{total_fetch}] Fetching {slug}...")
        filepath = STAGING_DIR / f"{slug}.html"

        try:
            response = session.get(url, timeout=30)
            http_code = response.status_code
            response.raise_for_status()

            content = response.content
            size = len(content)
            size_kb = size / 1024

            filepath.write_bytes(content)

            if size < 2048:
                status = "STUB"
                print(f"  [{i}/{total_fetch}] STUB - {size_kb:.1f} KB")
            elif size < 10240:
                status = "SMALL"
                print(f"  [{i}/{total_fetch}] SMALL - {size_kb:.0f} KB")
            else:
                status = "OK"
                print(f"  [{i}/{total_fetch}] OK - {size_kb:.0f} KB")

            results.append({
                "cat": cat, "slug": slug, "url": url,
                "size_kb": size_kb, "status": status,
                "http": str(http_code), "reason": "",
            })

        except requests.exceptions.HTTPError as e:
            code = e.response.status_code if e.response else "?"
            print(f"  [{i}/{total_fetch}] FAILED - HTTP {code}")
            results.append({
                "cat": cat, "slug": slug, "url": url,
                "size_kb": 0, "status": "FAILED",
                "http": str(code), "reason": f"HTTP {code}",
            })
        except requests.exceptions.ConnectionError:
            print(f"  [{i}/{total_fetch}] FAILED - connection error")
            results.append({
                "cat": cat, "slug": slug, "url": url,
                "size_kb": 0, "status": "FAILED",
                "http": "-", "reason": "connection error",
            })
        except requests.exceptions.Timeout:
            print(f"  [{i}/{total_fetch}] FAILED - timeout")
            results.append({
                "cat": cat, "slug": slug, "url": url,
                "size_kb": 0, "status": "FAILED",
                "http": "-", "reason": "timeout",
            })
        except Exception as e:
            print(f"  [{i}/{total_fetch}] FAILED - {e}")
            results.append({
                "cat": cat, "slug": slug, "url": url,
                "size_kb": 0, "status": "FAILED",
                "http": "-", "reason": str(e)[:80],
            })

        if i < total_fetch:
            time.sleep(1.5)

    # Sort by cat, then slug
    results.sort(key=lambda r: (r["cat"], r["slug"]))

    # Print summary table
    print()
    print("=" * 100)
    print("COMBINED FETCH RESULTS")
    print("=" * 100)
    print(f"  {'Cat':>3s}  {'Slug':<38s} {'HTTP':>4s} {'Size':>8s}  {'Status':<7s} {'Notes'}")
    print(f"  {'---':>3s}  {'---':<38s} {'---':>4s} {'---':>8s}  {'---':<7s} {'---'}")

    current_cat = None
    for r in results:
        if r["cat"] != current_cat:
            if current_cat is not None:
                print()
            current_cat = r["cat"]
        size_str = f"{r['size_kb']:.0f} KB" if r["size_kb"] > 0 else "-"
        notes = r["reason"] if r["status"] == "FAILED" else ""
        print(f"  {r['cat']:3d}  {r['slug']:<38s} {r['http']:>4s} {size_str:>8s}  {r['status']:<7s} {notes}")

    # Counts
    ok = sum(1 for r in results if r["status"] == "OK")
    skip = sum(1 for r in results if r["status"] == "SKIP")
    small = sum(1 for r in results if r["status"] == "SMALL")
    stub = sum(1 for r in results if r["status"] == "STUB")
    failed = sum(1 for r in results if r["status"] == "FAILED")
    total = len(results)

    print()
    print(f"  OK: {ok}  SKIP: {skip}  SMALL: {small}  STUB: {stub}  FAILED: {failed}  Total: {total}")
    print()

    # Categories with zero survivors
    cat_survivors = {}
    for r in results:
        if r["cat"] not in cat_survivors:
            cat_survivors[r["cat"]] = 0
        if r["status"] in ("OK", "SKIP", "SMALL"):
            cat_survivors[r["cat"]] += 1

    zero_cats = [c for c, n in sorted(cat_survivors.items()) if n == 0]
    if zero_cats:
        print(f"  Categories with ZERO survivors: {zero_cats}")
    else:
        print("  All categories have at least one survivor.")

    # Per-cat summary
    print()
    print("  Per-category:")
    for cat in sorted(cat_survivors.keys()):
        cat_results = [r for r in results if r["cat"] == cat]
        cat_ok = sum(1 for r in cat_results if r["status"] in ("OK", "SKIP"))
        cat_small = sum(1 for r in cat_results if r["status"] == "SMALL")
        cat_stub = sum(1 for r in cat_results if r["status"] == "STUB")
        cat_fail = sum(1 for r in cat_results if r["status"] == "FAILED")
        print(f"    Cat {cat:2d}: {len(cat_results):2d} total, {cat_ok} OK/SKIP, {cat_small} SMALL, {cat_stub} STUB, {cat_fail} FAILED")

    # Save to file
    lines = []
    lines.append("Mega-Fetch Combined Results")
    lines.append(f"Date: {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total entries: {len(URLS)}, After dedup: {len(deduped)}, Skipped (cached): {len(skipped)}, Fetched: {total_fetch}")
    lines.append("")
    lines.append(f"{'Cat':>3s}  {'Slug':<38s} {'HTTP':>4s} {'Size':>8s}  {'Status':<7s} {'Notes'}")
    lines.append(f"{'---':>3s}  {'---':<38s} {'---':>4s} {'---':>8s}  {'---':<7s} {'---'}")
    current_cat = None
    for r in results:
        if r["cat"] != current_cat:
            if current_cat is not None:
                lines.append("")
            current_cat = r["cat"]
        size_str = f"{r['size_kb']:.0f} KB" if r["size_kb"] > 0 else "-"
        notes = r["reason"] if r["status"] == "FAILED" else ""
        lines.append(f"{r['cat']:3d}  {r['slug']:<38s} {r['http']:>4s} {size_str:>8s}  {r['status']:<7s} {notes}")
    lines.append("")
    lines.append(f"OK: {ok}  SKIP: {skip}  SMALL: {small}  STUB: {stub}  FAILED: {failed}  Total: {total}")
    lines.append("")

    RESULTS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
