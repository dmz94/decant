# FLOWDOC V1 PLAN (REVISED)

## Step 1 — Lock scope in writing

Create SCOPE.md and freeze it for v1:

* **Project name:** Flowdoc
* **What:** General-purpose document converter for dyslexia-friendly output
* **Goal:** Convert any structured document into dyslexia-friendly, readable formats
* **Use cases:** Recipes, articles, manuals, educational content, work docs, instructions, technical documentation - any text-based structured content
* **Tier-1 input (v1):** HTML with semantic structure
  - **REQUIRED:** Must contain h1-h6, p, ul, ol elements (semantic HTML, not div soup)
  - **SUPPORTED:** Headings, paragraphs, lists, blockquotes, code blocks, inline emphasis/strong/code/links
  - **NOT SUPPORTED:** Pure div-based layouts with no semantic tags
* **Output (v1):** Readable HTML (canonical, self-contained, portable)
* **Design principle:** Readability over fidelity
  - **NO attempt to preserve original layout or branding**
  - **Focus:** Typography, spacing, structure for dyslexic readers
  - **Outcome:** Content may look completely different; that's the point
* **Non-goals:** PDF input, PDF output (v1 - deferred to v2), layout preservation, GUI, cloud service, recipe-specific features, image processing

**Key scope clarifications:**
- **PDF output is deferred to v2.** Browser print-to-PDF is sufficient for v1 and preserves CSS.
- **Semantic HTML is required.** Flowdoc will reject div soup with a clear error.
- **Readability trumps fidelity.** Original visual design is not preserved.

## Step 1.5 — Research typography guidelines

Read British Dyslexia Association Style Guide for typography recommendations.

Document findings in `docs/decisions.md`:
* Font choices and justification
* Line height, spacing, margins
* Color/contrast recommendations
* Sources and research backing decisions

## Step 2 — Create GitHub repo

* **Repo name:** flowdoc
* **License:** MIT

### Create files:

**README.md:**
- Elevator pitch: "Flowdoc converts structured documents into dyslexia-friendly, readable formats"
- Keep short (elevator pitch + quick start)
- Emphasize general-purpose: works on any structured text document
- Examples: recipes, articles, manuals, educational materials, work docs
- Input/output formats
- Use cases
- NOT positioned as recipe tool
- Push policy/rationale to SCOPE.md and docs/decisions.md

**SCOPE.md:**
- **Explicit scope boundaries**
- What Flowdoc is (general document converter)
- What it isn't (recipe manager, PDF fixer, layout tool)
- **Semantic HTML requirement:** Input must contain h1-h6, p, ul, ol (not div soup)
- **Readability over fidelity:** No attempt to preserve original layout/branding
- v1 inputs/outputs
- Non-goals clearly stated
- **PDF output:** Deferred to v2; v1 uses browser print-to-PDF (sufficient, preserves CSS)

**docs/decisions.md:**
- Why HTML first (semantic structure already present)
- Why general semantic model, not domain-specific
- Typography research and BDA sources
- **Font decision:** System fonts (Arial/Verdana) default; OpenDyslexic as only v1 toggle
- **Font licensing:** OpenDyslexic SIL-OFL allows embedding
- Why PDF is output format (v2), not input
- **Main content selection rule:** `<main>` → `<article>` → `<body>`
- **Firm policies for unsupported HTML elements** (tables, images, nav, footnotes, etc.)
- **Inline element handling:** whitespace preservation, nesting rules
- **HTML sanitization:** scripts, event handlers, active content dropped
- **Typography constants:** Modest CSS defaults (0.02em letter-spacing, 0.16em word-spacing) validated via feedback
- **CSS invariants:** Requirements for layout, spacing, color, links, print
- **CLI failure semantics:** Exit codes, error handling, non-semantic input rejection

**samples/:**
- Recipe HTML files
- Article or blog post
- How-to/instructional content
- Educational material
- Technical documentation sample
- Demonstrates breadth from day one

**src/:**
- Empty initially (signals intent, keeps root clean)

**tests/:**
- Empty initially (signals fixtures will be exercised)

**LICENSE:**
- MIT

**.gitignore:**
- Standard ignores for future tech stack

### GitHub settings (configure on day 1):

**Security (enable immediately):**
- Secret scanning + push protection
- Dependabot alerts and security updates

**Branch protection (on `main`):**
- Require pull request before merging
- Require 1 approval (when collaborators join)
- Require status checks to pass (add once CI exists)

**Templates:**
- PR template (keeps reviews focused)
- Issue templates (bug, feature)

**Defer until needed:**
- CodeQL scanning (enable once real code in `src/`)
- CODEOWNERS file (add when review responsibilities are clear)
- Signed commits (optional, adds friction early)

## Step 3 — Define minimal internal model

Document model - enough for recipes and general documents:

```
Document
  - title
  - sections[]
    - heading
    - blocks[]
      - paragraph (contains inline elements)
      - ordered_list (items contain inline elements)
      - unordered_list (items contain inline elements)
      - preformatted (code/pre blocks)
      - quote (blockquote, contains inline elements)

Inline elements (within paragraphs, list items, quotes):
  - text (plain text)
  - emphasis (em, i)
  - strong (strong, b)
  - code (inline code)
  - link (a with href and text)
```

**Critical:** Inline elements must be modeled explicitly. Without this, you'll either:
- Drop `<em>`, `<strong>`, `<code>`, `<a>` silently (data loss)
- Leak raw HTML into paragraphs (breaks rendering)

Both outcomes kill trust for technical/work documents.

**CRITICAL: Font decision for v1**

**Default font: System fonts (Arial/Verdana)**
- Universally available
- No licensing concerns
- No embedding needed
- Works everywhere immediately
- Layout-portable, not pixel-identical rendering

**v1 font toggle: OpenDyslexic only**
- OpenDyslexic (SIL Open Font License) is the ONLY alternative font in v1
- Accessed via `--font opendyslexic` CLI flag
- When selected: embedded as base64 in CSS for self-contained output
- When not selected: no font embedding
- Research shows no universal speed/accuracy improvement, but individual preference varies
- Included as user option, NOT as default or recommendation

**v1 scope control:**
- Do NOT add multiple font options in v1
- Additional fonts (Lexend, Atkinson Hyperlegible, Dyslexie) deferred to v2
- Keep font choice binary: system or OpenDyslexic

**Portability with this approach:**
- System fonts: self-contained HTML, consistent layout, font rendering varies by platform
- OpenDyslexic: self-contained HTML, pixel-identical rendering everywhere
- Both produce portable output

**Added blocks:**
- `preformatted` prevents mangling code/technical content
- `quote` handles blockquotes already parsed in Step 4
- These prevent silently dropping content or flattening structure

## Step 3.5 — Architecture & Tech Stack

Lock architectural and runtime decisions before implementation.

**Required decisions:**
1. Runtime/language choice (Python, Node.js, Go, Rust)
2. Specific parsing and sanitization libraries
3. Module architecture (parser/model/renderer separation)
4. Testing strategy (golden files, model snapshots, fixtures)
5. CLI specification (commands, flags, IO contracts, exit codes)
6. Library API surface for embedding

**Rationale:**
Implementing Step 4 (parser) before locking architecture risks rework when building Step 5 (renderer). Renderer requirements may expose parser design issues.

**Deliverable:**
Add new section to decisions.md titled "Step 3.5 — Architecture & Tech Stack" containing all finalized decisions with justifications.

**Constraint validation:**
Before proceeding to Step 4, verify architecture supports determinism, clean separation, embedding capability, and security requirements.

## Step 4 — Implement HTML → model

### Main content selection (deterministic)

Define how to choose "main content" to avoid subjective interpretation:

**v1 rule:**
1. If `<main>` exists, use it
2. Else if `<article>` exists, use it
3. Else use `<body>`

Parse only the selected main content area. Drop everything else (nav, header, footer, sidebar, aside).

### Parse semantic structure

* Extract title (from `<title>` or first `<h1>`)
* Parse h1-h6 headings
* Parse p, ul, ol, blockquote, pre/code
* **Parse inline elements:** em, strong, code (inline), a (with href)
* **Do NOT optimize for patterns specific to any particular app or source**
* Use whatever HTML files you have as test cases only
* Hard-code assumptions but comment them clearly

### Inline element handling (critical gotchas)

**Whitespace normalization:**
- Preserve whitespace across inline element boundaries
- Example: `word<strong>next</strong>` must render as "word next" not "wordnext"
- Apply standard HTML whitespace collapsing rules

**Nested inline tags:**
- Support one level of nesting (e.g., `<strong>` inside `<a>`)
- Flatten deeper nesting with consistent rule: preserve innermost semantic meaning
- Example: `<a><strong><em>text</em></strong></a>` → treat as strong emphasized link

### HTML sanitization (security)

Because HTML in → HTML out, apply strict sanitization:

**Drop entirely:**
- `<script>` tags and content
- Event handlers (onclick, onload, etc.)
- `<iframe>`, `<object>`, `<embed>`
- Active content of any kind

**Attributes:**
- Keep only semantic attributes needed for model (href for links)
- Drop style, class, id, data-* attributes
- Drop all event handler attributes

**Goal:** Prevent script injection and avoid leaking junk into output.

### Firm policies for unsupported elements

**v1 defaults** (deterministic, no ambiguity):

**Tables:** 
- Drop with placeholder: `[Table omitted - X rows, Y columns]`
- **Row count:** Number of `<tr>` elements
- **Column count:** Maximum number of immediate `<td>`/`<th>` children in any row
- **Ignore:** rowspan, colspan for counting purposes
- Do NOT attempt conversion in v1

**Images:**
- **If alt text exists:** `[Image: alt text here]`
- **If alt is missing or empty:** `[Image omitted]`
- Drop the image itself in both cases
- Preserve semantic meaning via alt text when available

**Navigation/sidebars/footers:**
- Drop entirely (handled by main content selection rule)
- Elements: `<nav>`, `<header>`, `<footer>`, `<aside>`

**Inline code:**
- Preserve as inline `<code>` styling within paragraphs
- Only create `preformatted` block for standalone code blocks (`<pre>`)

**Figures/captions:**
- Keep caption text as paragraph (from `<figcaption>`)
- Handle embedded image per image policy (alt text placeholder)

**Footnotes/endnotes:**
- Convert to regular paragraphs at point of reference
- Drop footnote markers/links

**Horizontal rules (`<hr>`):**
- Convert to visual separator (CSS border or spacing)

**Definition lists (`<dl>`):**
- Convert to unordered list with term + definition as list items

**Forms/inputs:**
- Drop with placeholder: `[Form omitted]`

**Goal:** Every unsupported element has a deterministic, predictable outcome.

## Step 5 — Implement renderer + CSS

Create readable HTML output:

* `template.html`
* `flowdoc.css` with dyslexia-friendly defaults
* **CRITICAL:** Inline all CSS and fonts into single self-contained HTML
* Output one HTML file with zero external dependencies

### CSS Invariants (Requirements, Not Suggestions)

Based on BDA typography guidelines, these are **mandatory** for v1:

**Typography:**
- Font: Arial or Verdana (or chosen alternative from Step 3)
- Font size: 16-19px body (BDA baseline; larger improves readability)
- Line height: 1.5 (150%) - BDA recommendation
- Letter spacing: Start with `letter-spacing: 0.02em`
- Word spacing: Start with `word-spacing: 0.16em`
- **Validation required:** Tune spacing based on dyslexic reader feedback; modest defaults are safer than aggressive spacing

**Layout (non-negotiable):**
- **Max line width:** 60-70 characters (prevents eye-tracking fatigue)
- **Generous margins:** Minimum 2em on sides, 1.5em top/bottom
- **Single-column layout:** No multi-column text
- **Left-aligned text:** No full justification
- **Ragged right edge:** Natural line breaks

**Spacing (requirements):**
- **Heading hierarchy:** Headings minimum 20% larger than body, bold weight
- **Paragraph spacing:** Minimum 1em between paragraphs
- **Heading spacing:** Minimum 1.5em before headings, 0.5em after
- **List indentation:** Clear nesting, minimum 2em indent per level
- **Whitespace:** Adequate padding throughout, no cramped layouts

**Color (requirements):**
- **Background:** Cream/off-white (#FEFCF4 or similar), NOT pure white (#FFFFFF)
- **Text:** Dark gray/black (#333333 or darker)
- **Contrast ratio:** WCAG AA minimum (4.5:1 normal text, 3:1 large text)
- **No patterns:** Solid backgrounds only

**Links (requirements):**
- **Screen:** Clearly differentiated (underline or distinct color + underline)
- **Print:** Remain identifiable (underline preserved, color may not print)
- **No link colors that fail contrast requirements**

**Print styles (requirements):**
- **Font size:** Do NOT shrink below 12pt
- **Line breaks:** Avoid orphaned list items or broken headings
- **Margins:** Adequate for binding/punching
- **Contrast:** Preserve on black-and-white printers

**These are not suggestions.** Violating these requirements defeats the purpose of dyslexia-friendly output.

## Step 6 — Add CLI wrapper

Basic command-line interface:

```bash
flowdoc convert input.html
flowdoc convert input.html -o output.html
flowdoc convert input.html --output output.html
```

### CLI options for v1

**Will ship:**
```bash
flowdoc convert input.html [-o output.html]
--font opendyslexic              # Use OpenDyslexic instead of system font
```

**Defer to v2:**
```bash
--theme [default|high-contrast]  # Needs design work beyond v1
```

### OpenDyslexic font toggle (v1 explicit decision)

**Policy:**
- OpenDyslexic is supported as a user toggle via `--font opendyslexic`
- OpenDyslexic is NOT the default
- Flowdoc makes NO claim that OpenDyslexic is universally better
- Included because individual preference varies

**Implementation:**
- If `--font opendyslexic` specified: embed OpenDyslexic font as base64 in CSS
- If not specified: use system font stack (Arial, Verdana), embed nothing
- Output remains self-contained in both cases

**Scope control:**
- OpenDyslexic is the ONLY v1 font option beyond system fonts
- Additional fonts (Lexend, Dyslexie, Atkinson Hyperlegible) deferred to v2
- Do not expand into "multiple font toggles" in v1

### CLI failure semantics

**Exit codes:**
- `0` - Success
- `1` - Parse error (malformed HTML, can't extract main content)
- `2` - Render error (internal failure generating output)
- `3` - I/O error (can't read input or write output)

**Error handling:**
- All errors to stderr
- Stdout contains only output HTML (or nothing on failure)

**Non-semantic HTML input:**
- If input lacks semantic structure (no headings, no paragraphs, only divs):
  - Hard fail with clear error message
  - Exit code 1
  - Error: "Input HTML lacks semantic structure (no headings, paragraphs, or lists found)"
- Do NOT attempt best-effort conversion of div soup

## Step 7 — Create test suite

Build test cases covering different document types and failure modes:

### Required test fixtures (must include all of these):

1. **Recipe** - Basic semantic structure
2. **Article/blog post** - Typical web content
3. **Technical documentation** - Code blocks, inline code, links
4. **Instructional content** - How-to with numbered steps
5. **List-heavy document** - Nested lists, mixed ordered/unordered
6. **Document with quotes/blockquotes** - Block quotes, citations
7. **Document with emphasis/inline elements** - Heavy use of em, strong, inline code, links
8. **Main content selection test** - Has header, nav, footer, sidebar PLUS `<main>` or `<article>`
9. **Inline handling stress test** - Dense inline emphasis/links/code, tests whitespace preservation
10. **Edge case document** - Image with missing alt + table with colspan/rowspan

**Coverage requirements:**
- Main content selection (fixtures 8)
- Inline elements and whitespace (fixtures 7, 9)
- Unsupported element degradation (fixtures 10)
- Block elements (fixtures 6)
- All fixtures must use real-world HTML (not hand-crafted minimal examples)

### Add snapshot testing

Beyond visual inspection, add automated regression prevention:

**Model snapshot tests:**
- Assert internal model JSON for each fixture
- Stable, fast, prevents regressions in parsing
- Catches "one parser tweak broke list nesting everywhere" failures

**Rendered HTML snapshots (optional):**
- Snapshot of rendered HTML after minifying/normalizing whitespace
- Validates rendering consistency

Convert all fixtures, visually inspect results, catch obvious failures.

## Step 8a — Test with dyslexic readers

Share output with Colin and Cameron:

* Test on multiple devices: phone, tablet, desktop
* Print and test on paper
* Test both with and without OpenDyslexic font
* Validate core value before proceeding

### Concrete feedback questions

Give testers a structured checklist for actionable feedback:

1. **Navigation:** Where did you lose your place while reading?
2. **Visual fatigue:** What felt visually tiring or difficult?
3. **Scannability:** Were headings and lists easy to scan?
4. **Device differences:** Any issues on phone vs desktop vs tablet?
5. **Print quality:** What broke or looked wrong when printed?
6. **Overall:** Is this actually better? More readable? Less fatiguing?
7. **Font preference:** OpenDyslexic on or off? (Collects preference data without making efficacy claims)

Higher-signal feedback than "looks good / looks bad."

**Note:** Font preference question is about individual preference, NOT a research claim about OpenDyslexic efficacy.

## Step 8b — Code and architecture review

Ask Colin and Cameron for:

* Code review
* Architecture feedback
* Internal model evaluation (too narrow? too broad?)
* Error handling suggestions

## Step 9 — Plan v2 (only after v1 works end-to-end)

After v1 validates core value, consider expansion in two directions:

### Additional Input Formats
- Markdown importer (easy win - straightforward parsing)
- DOCX importer (via libraries like python-docx or mammoth)

### Additional Output Formats
- **PDF generation** (if browser print-to-PDF proves insufficient)
  - Via headless Chrome (Playwright/Puppeteer)
  - Or standalone tools (wkhtmltopdf, weasyprint)
  - Typography decisions transfer directly via CSS
- **DOCX output** (font stack, sizing, spacing apply via document styles)

### Content Transformation Features

Based on BDA writing style guidance, extend Flowdoc from format-only conversion to content improvement:

**Text-to-Speech (TTS) Compatibility:**
- Add punctuation after bullet points (semicolons, commas, periods) for TTS pauses
- Remove/replace symbols spoken awkwardly (asterisks, long dashes, special chars)
- Avoid ALL CAPS mid-sentence (TTS may read as individual letters)
- Replace automatic numbering (some screen readers skip these)

**Readability Enhancement:**
- Readability scoring against BDA plain language principles
- Sentence simplification (break long sentences, passive → active voice)
- Jargon expansion (detect abbreviations, provide expanded forms on first use)
- Paragraph breaking (split dense text blocks into shorter, spaced paragraphs)
- Symbol cleanup (remove/replace characters interfering with TTS/screen readers)

### Optional Enhancements
- Additional font options beyond OpenDyslexic (Lexend, Atkinson Hyperlegible, Dyslexie)
- Configurable themes beyond high-contrast
- Local web preview mode
- Batch conversion support

**DO NOT plan v2 details now.** This is scope for consideration after v1 proves value.

---

## Key Discipline

At every step, ask:

**"Does this help produce a readable document for a dyslexic reader?"**

If no, it's out of scope.

---

## Success Criteria for v1

1. Takes an HTML file with semantic structure
2. Produces a self-contained, readable HTML file
3. **Output is measurably better for dyslexic readers:**
   - **Primary test:** Readers complete a 2-3 minute reading task with fewer re-reads and fewer line-loss events vs original formatting
   - **Validation checklist:** Readers report lower visual fatigue and better place-keeping on structured feedback form
   - **Honesty check:** Identify at least one reading scenario where v1 output is NOT better (prevents over-claiming)
4. Works reliably across devices (phone, tablet, desktop) and print
5. Command-line interface is simple and functional
6. Font licensing is clear and documented
7. Failure modes are predictable and consistent
8. Inline elements (links, emphasis, code) render correctly
9. Unsupported elements (tables, images) degrade gracefully per defined policy

If v1 meets these criteria, scope expansion is justified.  
If not, scope expansion is premature.
