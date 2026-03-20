/**
 * Run Readability.js on a local HTML fixture and save extracted content.
 *
 * Usage:
 *   node scripts/readability-extract.js <fixture-path> <output-path>
 *
 * Outputs:
 *   - <output-path>: the clean article HTML
 *   - <output-path>.json: metadata sidecar (title, byline, excerpt, etc.)
 */

const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");
const { Readability } = require("@mozilla/readability");

// Source URLs for fixtures (keyed by filename stem).
// Expand as needed; only yale360-baboons is wired up for now.
const SOURCE_URLS = {
  "yale360-baboons": "https://e360.yale.edu/features/cape-town-baboons",
  "timeout-london": "https://www.timeout.com/london/things-to-do/101-things-to-do-in-london",
  "atavist-castles": "https://magazine.atavist.com/2020/castles-in-the-sky-san-francisco-denmark-diary-love-mystery",
  "nature-comms": "https://www.nature.com/articles/s41467-024-50779-y",
  "bleacherreport-bracket": "https://bleacherreport.com/articles/25407372-ncaa-tournament-2026-predictions-mens-sweet-16-bracket-after-selection-sunday",
};

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error("Usage: node readability-extract.js <fixture-path> <output-path> [--source-url=URL]");
  process.exit(1);
}

const fixturePath = args[0];
const outputPath = args[1];

const html = fs.readFileSync(fixturePath, "utf-8");

// Derive slug from filename to look up source URL; --source-url overrides
const stem = path.basename(fixturePath, ".html");
let sourceUrl = SOURCE_URLS[stem] || "https://example.com/placeholder";
for (const arg of args.slice(2)) {
  if (arg.startsWith("--source-url=")) {
    sourceUrl = arg.slice("--source-url=".length);
  }
}

const dom = new JSDOM(html, { url: sourceUrl });
const reader = new Readability(dom.window.document);
const article = reader.parse();

if (!article) {
  console.error("Readability returned null -- could not parse article.");
  process.exit(1);
}

// Write article HTML
fs.writeFileSync(outputPath, article.content, "utf-8");

// Write metadata sidecar
const sidecar = {
  title: article.title,
  byline: article.byline,
  excerpt: article.excerpt,
  siteName: article.siteName,
  lang: article.lang,
  length: article.length,
};
const jsonPath = outputPath.replace(/\.html$/, ".json");
fs.writeFileSync(jsonPath, JSON.stringify(sidecar, null, 2), "utf-8");

// Check for images
const imageCount = (article.content.match(/<img[\s>]/gi) || []).length;

console.log(
  `Title: ${article.title} | Length: ${article.length} chars | Images: ${imageCount}`
);
