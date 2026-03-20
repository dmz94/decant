"""
Compare Readability.js extraction against Decant extraction for the same fixture.

Usage:
    node scripts/readability-extract.js <fixture> /tmp/readability-output.html
    python scripts/compare-extractions.py <fixture> /tmp/readability-output.html

Generates an HTML review page in tests/corpus-screening/review/.
"""
import difflib
import html as html_module
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Decant pipeline (same pattern as screening tool)
# ---------------------------------------------------------------------------

from decant.core.content_selector import detect_mode
from decant.core.parser import parse, extract_with_trafilatura
from decant.core.renderer import render


def run_decant_pipeline(fixture_path: Path) -> str:
    """Run Decant pipeline on fixture, return rendered HTML."""
    html = fixture_path.read_text(encoding="utf-8", errors="replace")
    mode = detect_mode(html)

    original_title = None
    html_to_parse = html

    if mode == "extract":
        original_soup = BeautifulSoup(html, "lxml")
        original_title = original_soup.find("title")
        html_to_parse = extract_with_trafilatura(html)

    doc = parse(
        html_to_parse,
        original_title=original_title,
        require_article_body=(mode == "extract"),
    )
    return render(doc)


# ---------------------------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------------------------

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote", "pre"}


def extract_paragraphs(html_str: str) -> list[str]:
    """Extract ordered text fragments from block elements."""
    soup = BeautifulSoup(html_str, "lxml")
    paragraphs = []
    for tag in soup.find_all(BLOCK_TAGS):
        text = tag.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 20:
            paragraphs.append(text)
    return paragraphs


def extract_headings(html_str: str) -> list[tuple[int, str]]:
    """Extract heading outline as (level, text) tuples."""
    soup = BeautifulSoup(html_str, "lxml")
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(tag.name[1])
        text = tag.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            headings.append((level, text))
    return headings


def extract_images(html_str: str, base_url: str = "") -> list[dict]:
    """Extract image info: src, alt."""
    soup = BeautifulSoup(html_str, "lxml")
    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if base_url and src and not src.startswith(("http://", "https://", "data:")):
            src = urljoin(base_url, src)
        alt = img.get("alt", "")
        images.append({"src": src, "alt": alt})
    return images


def count_elements(html_str: str, tags: list[str]) -> int:
    """Count top-level occurrences of given tags."""
    soup = BeautifulSoup(html_str, "lxml")
    return len(soup.find_all(tags))


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def compare_paragraphs(readability_paras, decant_paras):
    """Classify paragraphs as BOTH, READABILITY_ONLY, or DECANT_ONLY."""
    sm = difflib.SequenceMatcher(None, readability_paras, decant_paras)
    ratio = sm.ratio()

    classified = []

    # Build sets for quick lookup using normalized text
    def normalize(t):
        return re.sub(r"\s+", "", t.lower())

    r_norm = {normalize(p): p for p in readability_paras}
    d_norm = {normalize(p): p for p in decant_paras}
    r_norm_set = set(r_norm.keys())
    d_norm_set = set(d_norm.keys())

    both_norm = r_norm_set & d_norm_set
    r_only_norm = r_norm_set - d_norm_set
    d_only_norm = d_norm_set - r_norm_set

    # Preserve order from readability
    seen = set()
    for p in readability_paras:
        n = normalize(p)
        if n in seen:
            continue
        seen.add(n)
        if n in both_norm:
            classified.append(("BOTH", p))
        else:
            classified.append(("READABILITY_ONLY", p))

    for p in decant_paras:
        n = normalize(p)
        if n not in seen:
            seen.add(n)
            classified.append(("DECANT_ONLY", p))

    return classified, ratio


def compare_headings(r_headings, d_headings):
    """Compare heading outlines."""
    r_texts = [f"h{lvl}: {txt}" for lvl, txt in r_headings]
    d_texts = [f"h{lvl}: {txt}" for lvl, txt in d_headings]
    sm = difflib.SequenceMatcher(None, r_texts, d_texts)
    return r_texts, d_texts, sm.ratio()


def compare_images(r_images, d_images):
    """Classify images by src presence."""
    r_srcs = {img["src"] for img in r_images if img["src"]}
    d_srcs = {img["src"] for img in d_images if img["src"]}

    classified = []
    for img in r_images:
        if not img["src"]:
            continue
        status = "BOTH" if img["src"] in d_srcs else "READABILITY_ONLY"
        classified.append((status, img))

    for img in d_images:
        if not img["src"]:
            continue
        if img["src"] not in r_srcs:
            classified.append(("DECANT_ONLY", img))

    return classified


# ---------------------------------------------------------------------------
# HTML report generation
# ---------------------------------------------------------------------------

def truncate(text: str, length: int = 80) -> str:
    if len(text) <= length:
        return text
    return text[:length] + "..."


def generate_report(
    fixture_name: str,
    readability_html: str,
    decant_html: str,
    readability_meta: dict,
    classified_paras: list,
    para_ratio: float,
    r_headings_text: list,
    d_headings_text: list,
    heading_ratio: float,
    classified_images: list,
    r_table_count: int,
    d_table_count: int,
    r_list_count: int,
    d_list_count: int,
) -> str:
    """Generate a comparison HTML report."""

    # Counts
    both_count = sum(1 for s, _ in classified_paras if s == "BOTH")
    r_only_count = sum(1 for s, _ in classified_paras if s == "READABILITY_ONLY")
    d_only_count = sum(1 for s, _ in classified_paras if s == "DECANT_ONLY")
    r_img_only = sum(1 for s, _ in classified_images if s == "READABILITY_ONLY")
    d_img_only = sum(1 for s, _ in classified_images if s == "DECANT_ONLY")
    both_img = sum(1 for s, _ in classified_images if s == "BOTH")

    # Para diff rows
    para_rows = []
    for status, text in classified_paras:
        escaped = html_module.escape(text)
        short = html_module.escape(truncate(text))
        if status == "BOTH":
            color = "#e8f5e9"
            label = "Both"
        elif status == "READABILITY_ONLY":
            color = "#ffebee"
            label = "Readability only"
        else:
            color = "#fff3e0"
            label = "Decant only"
        para_rows.append(
            f'<tr style="background:{color};">'
            f'<td style="padding:4px 8px;font-size:12px;white-space:nowrap;">{label}</td>'
            f'<td style="padding:4px 8px;font-size:12px;" title="{escaped}">{short}</td>'
            f'</tr>'
        )
    para_table = "\n".join(para_rows)

    # Heading diff
    heading_rows = []
    max_len = max(len(r_headings_text), len(d_headings_text))
    for i in range(max_len):
        r_h = html_module.escape(r_headings_text[i]) if i < len(r_headings_text) else '<span style="color:#aaa;">—</span>'
        d_h = html_module.escape(d_headings_text[i]) if i < len(d_headings_text) else '<span style="color:#aaa;">—</span>'
        heading_rows.append(
            f'<tr><td style="padding:4px 8px;font-size:12px;">{r_h}</td>'
            f'<td style="padding:4px 8px;font-size:12px;">{d_h}</td></tr>'
        )
    heading_table = "\n".join(heading_rows)

    # Image diff
    img_rows = []
    for status, img in classified_images:
        src_short = html_module.escape(truncate(img["src"], 60))
        alt = html_module.escape(img.get("alt", ""))
        if status == "BOTH":
            color = "#e8f5e9"
            label = "Both"
        elif status == "READABILITY_ONLY":
            color = "#ffebee"
            label = "Readability only"
        else:
            color = "#fff3e0"
            label = "Decant only"
        img_rows.append(
            f'<tr style="background:{color};">'
            f'<td style="padding:4px 8px;font-size:12px;">{label}</td>'
            f'<td style="padding:4px 8px;font-size:11px;word-break:break-all;">{src_short}</td>'
            f'<td style="padding:4px 8px;font-size:12px;">{alt}</td>'
            f'</tr>'
        )
    img_table = "\n".join(img_rows) if img_rows else '<tr><td colspan="3" style="padding:8px;color:#888;">No images in either extraction.</td></tr>'

    # Metadata
    meta_rows = []
    for key in ("title", "byline", "excerpt", "siteName", "lang", "length"):
        val = html_module.escape(str(readability_meta.get(key, "")))
        meta_rows.append(f'<tr><td style="padding:4px 8px;font-weight:600;">{key}</td><td style="padding:4px 8px;">{val}</td></tr>')
    meta_table = "\n".join(meta_rows)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compare: {html_module.escape(fixture_name)}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: system-ui, -apple-system, sans-serif; font-size: 14px; color: #333; background: #f5f5f5; padding: 1rem; }}
.card {{ max-width: 1100px; margin: 0 auto 1rem; background: #fff; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); padding: 1.5rem; }}
h1 {{ font-size: 1.3rem; margin-bottom: 1rem; }}
h2 {{ font-size: 1rem; margin: 1.5rem 0 0.5rem; padding-bottom: 0.3rem; border-bottom: 1px solid #ddd; }}
h2:first-of-type {{ margin-top: 0; }}
table {{ width: 100%; border-collapse: collapse; margin-bottom: 0.5rem; }}
th, td {{ border: 1px solid #ddd; text-align: left; vertical-align: top; }}
th {{ background: #f9f9f9; padding: 6px 8px; font-size: 12px; text-transform: uppercase; color: #555; }}
.stat {{ display: inline-block; background: #f0f0f0; border-radius: 4px; padding: 4px 10px; margin: 2px 4px 2px 0; font-size: 13px; }}
.stat strong {{ color: #1856a8; }}
.legend {{ font-size: 12px; color: #666; margin-bottom: 8px; }}
.legend span {{ display: inline-block; width: 12px; height: 12px; border-radius: 2px; vertical-align: middle; margin-right: 3px; }}
</style>
</head>
<body>

<div class="card">
<h1>Readability vs Decant: {html_module.escape(fixture_name)}</h1>

<h2>Summary</h2>
<div>
  <span class="stat">Similarity: <strong>{para_ratio:.1%}</strong></span>
  <span class="stat">Paragraphs: <strong>{both_count}</strong> shared, <strong>{r_only_count}</strong> Readability-only, <strong>{d_only_count}</strong> Decant-only</span>
</div>
<div style="margin-top: 4px;">
  <span class="stat">Headings: <strong>{len(r_headings_text)}</strong> R / <strong>{len(d_headings_text)}</strong> D (similarity {heading_ratio:.1%})</span>
  <span class="stat">Images: <strong>{both_img}</strong> shared, <strong>{r_img_only}</strong> R-only, <strong>{d_img_only}</strong> D-only</span>
  <span class="stat">Tables: <strong>{r_table_count}</strong> R / <strong>{d_table_count}</strong> D</span>
  <span class="stat">Lists: <strong>{r_list_count}</strong> R / <strong>{d_list_count}</strong> D</span>
</div>

<h2>Text Diff</h2>
<div class="legend">
  <span style="background:#e8f5e9;"></span> Both &nbsp;
  <span style="background:#ffebee;"></span> Readability only (Decant missed) &nbsp;
  <span style="background:#fff3e0;"></span> Decant only (possible boilerplate)
</div>
<table>
<tr><th style="width:120px;">Status</th><th>Text (hover for full)</th></tr>
{para_table}
</table>

<h2>Heading Outline</h2>
<table>
<tr><th>Readability</th><th>Decant</th></tr>
{heading_table}
</table>

<h2>Image Comparison</h2>
<table>
<tr><th style="width:120px;">Status</th><th>src</th><th>alt</th></tr>
{img_table}
</table>

<h2>Readability Metadata</h2>
<table>
<tr><th style="width:100px;">Field</th><th>Value</th></tr>
{meta_table}
</table>

</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Structured comparison (for batch runner / AI triage)
# ---------------------------------------------------------------------------

def run_comparison(fixture_path: Path, readability_html: str, readability_meta: dict) -> dict:
    """Run full comparison and return structured data + generate HTML report.

    Returns a dict with all comparison results for JSON serialization.
    Also generates the HTML review page as a side effect.
    """
    fixture_name = fixture_path.stem

    # Run Decant pipeline
    decant_html = run_decant_pipeline(fixture_path)

    # Compare text coverage
    r_paras = extract_paragraphs(readability_html)
    d_paras = extract_paragraphs(decant_html)
    classified_paras, para_ratio = compare_paragraphs(r_paras, d_paras)

    # Compare structure
    r_headings = extract_headings(readability_html)
    d_headings = extract_headings(decant_html)
    r_headings_text, d_headings_text, heading_ratio = compare_headings(r_headings, d_headings)

    r_table_count = count_elements(readability_html, ["table"])
    d_table_count = count_elements(decant_html, ["table"])
    r_list_count = count_elements(readability_html, ["ul", "ol"])
    d_list_count = count_elements(decant_html, ["ul", "ol"])

    # Compare images
    source_url = readability_meta.get("sourceUrl", "")
    r_images = extract_images(readability_html, source_url)
    d_images = extract_images(decant_html, source_url)
    classified_images = compare_images(r_images, d_images)

    # Generate HTML report
    review_dir = Path(__file__).resolve().parent.parent / "tests" / "corpus-screening" / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    report_path = review_dir / f"compare-{fixture_name}.html"

    report = generate_report(
        fixture_name=fixture_name,
        readability_html=readability_html,
        decant_html=decant_html,
        readability_meta=readability_meta,
        classified_paras=classified_paras,
        para_ratio=para_ratio,
        r_headings_text=r_headings_text,
        d_headings_text=d_headings_text,
        heading_ratio=heading_ratio,
        classified_images=classified_images,
        r_table_count=r_table_count,
        d_table_count=d_table_count,
        r_list_count=r_list_count,
        d_list_count=d_list_count,
    )
    report_path.write_text(report, encoding="utf-8")

    # Build structured result
    readability_only_texts = [p for s, p in classified_paras if s == "READABILITY_ONLY"]
    decant_only_texts = [p for s, p in classified_paras if s == "DECANT_ONLY"]

    r_only_imgs = [img for s, img in classified_images if s == "READABILITY_ONLY"]
    d_only_imgs = [img for s, img in classified_images if s == "DECANT_ONLY"]
    shared_imgs = [img for s, img in classified_images if s == "BOTH"]

    # Determine direction
    r_only_count = len(readability_only_texts)
    d_only_count = len(decant_only_texts)
    if d_only_count > r_only_count and (d_only_count - r_only_count) > 2:
        direction = "DECANT_AHEAD"
    elif r_only_count > d_only_count and (r_only_count - d_only_count) > 2:
        direction = "DECANT_BEHIND"
    else:
        direction = "COMPARABLE"

    return {
        "fixture": fixture_name,
        "similarity": round(para_ratio, 3),
        "direction": direction,
        "paragraphs": {
            "shared": sum(1 for s, _ in classified_paras if s == "BOTH"),
            "readability_only": r_only_count,
            "decant_only": d_only_count,
        },
        "readability_only_texts": readability_only_texts,
        "decant_only_texts": decant_only_texts,
        "headings": {
            "readability": [[f"h{lvl}", txt] for lvl, txt in r_headings],
            "decant": [[f"h{lvl}", txt] for lvl, txt in d_headings],
        },
        "images": {
            "readability_only": r_only_imgs,
            "decant_only": d_only_imgs,
            "shared": shared_imgs,
        },
        "tables": {"readability": r_table_count, "decant": d_table_count},
        "lists": {"readability": r_list_count, "decant": d_list_count},
        "report_path": str(report_path),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python compare-extractions.py <fixture-path> <readability-output-path>", file=sys.stderr)
        sys.exit(1)

    fixture_path = Path(sys.argv[1])
    readability_path = Path(sys.argv[2])

    fixture_name = fixture_path.stem

    # Run Decant pipeline
    print(f"Running Decant pipeline on {fixture_name}...")
    decant_html = run_decant_pipeline(fixture_path)
    decant_out = Path("/tmp/decant-output.html")
    decant_out.write_text(decant_html, encoding="utf-8")
    print(f"  Decant output saved to {decant_out}")

    # Load Readability output
    readability_html = readability_path.read_text(encoding="utf-8")
    json_path = readability_path.with_suffix(".json")
    readability_meta = {}
    if json_path.exists():
        readability_meta = json.loads(json_path.read_text(encoding="utf-8"))

    # Compare text coverage
    print("Comparing text coverage...")
    r_paras = extract_paragraphs(readability_html)
    d_paras = extract_paragraphs(decant_html)
    classified_paras, para_ratio = compare_paragraphs(r_paras, d_paras)

    # Compare structure
    print("Comparing structure...")
    r_headings = extract_headings(readability_html)
    d_headings = extract_headings(decant_html)
    r_headings_text, d_headings_text, heading_ratio = compare_headings(r_headings, d_headings)

    r_table_count = count_elements(readability_html, ["table"])
    d_table_count = count_elements(decant_html, ["table"])
    r_list_count = count_elements(readability_html, ["ul", "ol"])
    d_list_count = count_elements(decant_html, ["ul", "ol"])

    # Compare images
    print("Comparing images...")
    source_url = readability_meta.get("sourceUrl", "https://e360.yale.edu/features/cape-town-baboons")
    r_images = extract_images(readability_html, source_url)
    d_images = extract_images(decant_html, source_url)
    classified_images = compare_images(r_images, d_images)

    # Summary
    both_p = sum(1 for s, _ in classified_paras if s == "BOTH")
    r_only_p = sum(1 for s, _ in classified_paras if s == "READABILITY_ONLY")
    d_only_p = sum(1 for s, _ in classified_paras if s == "DECANT_ONLY")
    r_img_only = sum(1 for s, _ in classified_images if s == "READABILITY_ONLY")
    print(f"\nText similarity: {para_ratio:.1%}")
    print(f"Paragraphs: {both_p} shared, {r_only_p} Readability-only, {d_only_p} Decant-only")
    print(f"Headings: {len(r_headings)} R / {len(d_headings)} D")
    print(f"Images: {r_img_only} Readability-only, {sum(1 for s, _ in classified_images if s == 'DECANT_ONLY')} Decant-only")

    # Generate report
    print("\nGenerating report...")
    review_dir = Path(__file__).resolve().parent.parent / "tests" / "corpus-screening" / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    report_path = review_dir / f"compare-{fixture_name}.html"

    report = generate_report(
        fixture_name=fixture_name,
        readability_html=readability_html,
        decant_html=decant_html,
        readability_meta=readability_meta,
        classified_paras=classified_paras,
        para_ratio=para_ratio,
        r_headings_text=r_headings_text,
        d_headings_text=d_headings_text,
        heading_ratio=heading_ratio,
        classified_images=classified_images,
        r_table_count=r_table_count,
        d_table_count=d_table_count,
        r_list_count=r_list_count,
        d_list_count=d_list_count,
    )

    report_path.write_text(report, encoding="utf-8")
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
