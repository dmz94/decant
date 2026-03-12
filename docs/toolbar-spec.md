# Decant Toolbar Redesign Spec

Status: Ready for implementation
Date: 2026-03-12
Decisions by: Dave (product owner) + Opus (controller)
Implements: Chunks 4-6 of the surface build

This spec replaces the current right-side settings panel with a
Firefox-style vertical toolbar on the left side of the content
area. All existing settings functionality is preserved. New action
buttons are added. Chrome (toolbar, buttons, popouts) participates
in the active theme via CSS variables.

Reference: Firefox Reader Mode source (aboutReader.css,
aboutReader.html, AboutReader.sys.mjs) via searchfox.org.

---

## 1) Design Decisions (locked)

These were made in the Opus controller chat. Do not revisit.

D1: Replace the current right-side slide-out settings panel with
    a FF-style vertical icon toolbar + individual popout panels.
    One control surface, not two.

D2: Six icons in the toolbar strip (top to bottom):
    1. Aa -- text controls popout
    2. Theme icon -- theme picker popout
    3. Save icon -- popout with Print / Download HTML / Download PDF
    4. Share icon -- single action (copy URL to clipboard)
    5. View Original icon -- single action (open in new tab)
    6. ? icon -- help popout (info and links only)

D3: Chrome participates in the active theme. Toolbar border,
    icon fill, popup background, shadow all change per theme
    via CSS custom properties on the body element.

Visibility: Share and View Original are hidden (not disabled)
when the conversion source is a file upload. They appear only
for URL conversions. The Help popout mentions this.

---

## 2) Toolbar Structure (HTML)

The toolbar is a sticky container positioned to the left of the
content iframe. It takes up zero vertical space (height: 0) and
positions itself using negative margin, exactly like the FF
pattern.

```
<div id="toolbar-container" class="toolbar-container">
  <div class="toolbar">

    <!-- Text controls -->
    <ul class="dropdown text-dropdown">
      <li>
        <button class="dropdown-toggle toolbar-button text-button"
                aria-label="Text and layout settings">
          <span class="hover-label">Text</span>
        </button>
      </li>
      <li class="dropdown-popup" id="text-controls" tabindex="-1">
        <!-- text panel content, see section 4 -->
      </li>
    </ul>

    <!-- Theme picker -->
    <ul class="dropdown theme-dropdown">
      <li>
        <button class="dropdown-toggle toolbar-button theme-button"
                aria-label="Theme">
          <span class="hover-label">Theme</span>
        </button>
      </li>
      <li class="dropdown-popup" id="theme-controls" tabindex="-1">
        <!-- theme panel content, see section 5 -->
      </li>
    </ul>

    <!-- Save (Print / Download HTML / Download PDF) -->
    <ul class="dropdown save-dropdown">
      <li>
        <button class="dropdown-toggle toolbar-button save-button"
                aria-label="Save and print">
          <span class="hover-label">Save</span>
        </button>
      </li>
      <li class="dropdown-popup" id="save-controls" tabindex="-1">
        <!-- save panel content, see section 6 -->
      </li>
    </ul>

    <!-- Share (single action, URL conversions only) -->
    <button class="toolbar-button share-button"
            id="share-btn"
            aria-label="Copy share link">
      <span class="hover-label">Share</span>
    </button>

    <!-- View Original (single action, URL conversions only) -->
    <button class="toolbar-button view-original-button"
            id="view-original-btn"
            aria-label="View original page">
      <span class="hover-label">View Original</span>
    </button>

    <!-- Help / Feedback -->
    <ul class="dropdown help-dropdown">
      <li>
        <button class="dropdown-toggle toolbar-button help-button"
                aria-label="Help and feedback">
          <span class="hover-label">Help</span>
        </button>
      </li>
      <li class="dropdown-popup" id="help-controls" tabindex="-1">
        <!-- help panel content, see section 7 -->
      </li>
    </ul>

  </div>
</div>
```

Notes:
- Dropdown items use <ul> wrapper. Single-action items are plain
  <button> elements (no <ul> wrapper needed).
- Share and View Original buttons get a data attribute or class
  (e.g. "url-only") so JS can show/hide them based on conversion
  source.
- All buttons are 32x32px with 16x16px icon (SVG background
  image or inline SVG).

---

## 3) Toolbar Positioning (CSS)

```
.toolbar-container {
  position: sticky;
  z-index: 2;
  top: 32px;
  height: 0;
  font-family: system-ui, sans-serif;
}

.toolbar {
  padding-block: 16px;
  border: 1px solid var(--toolbar-border);
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--toolbar-shadow);
  width: 32px;
  padding-inline: 8px;
  background-color: var(--toolbar-bg);
  list-style: none;
  user-select: none;
}

.toolbar-button {
  position: relative;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 1px solid var(--toolbar-button-border);
  border-radius: 6px;
  margin: 4px 0;
  background-color: transparent;
  background-size: 16px 16px;
  background-position: center;
  background-repeat: no-repeat;
  cursor: pointer;
  color: var(--icon-fill);
  fill: var(--icon-fill);
}

.toolbar-button:hover {
  background-color: var(--toolbar-button-hover);
}

.toolbar-button:active,
.open .toolbar-button {
  background-color: var(--toolbar-button-active);
}
```

The toolbar-container positioning relative to the content area
must be determined by reading the current index.html layout.
The FF pattern uses negative margin-inline-start to position
the toolbar in the left gutter. Adapt to Decant's actual layout.

IMPORTANT: Sonnet must read the current index.html, app.css, and
app.js BEFORE implementing. Do not assume layout structure.

---

## 4) Text Controls Popout

Contains all current settings panel controls EXCEPT theme.

Panel width: 300-340px. Appears to the right of the toolbar.

Contents (top to bottom):

a) Font choice: 3 buttons in a row (Sans-serif, OpenDyslexic,
   Serif). Same pattern as current implementation.

b) Font size: slider. Current zoom-based implementation.
   Label: "Font size". Show current value.

c) Content width: 3 buttons (Narrow, Medium, Wide).
   Same pattern as current implementation.

d) Text spacing: 3 buttons (Standard, Loose, Very Loose).
   Same pattern as current implementation.

e) Reset to defaults: text button at bottom of panel.

All behavior (localStorage persistence, buildOverrideCSS,
iframe CSS injection) stays exactly as-is. Only the container
changes from a slide-out panel to a popout.

---

## 5) Theme Picker Popout

Panel width: ~260px. 2x2 grid of theme buttons.

Themes (unchanged from current):
- Light (white bg)
- Sepia (cream bg)
- Dark (dark bg)
- Contrast (black bg, high contrast)

Each button shows: color swatch square (4px border-radius) +
label text. Selected theme gets a highlighted border or
background.

The theme picker panel itself adapts to the current theme
(see section 8 for token values).

---

## 6) Save Popout

Panel width: ~200px. Three stacked buttons:

- Print -- triggers window.print() on iframe content
- Download HTML -- serves converted HTML as file download
- Download PDF -- POST /convert/pdf (server-side weasyprint)

Each button is a full-width text button with an icon on the
left. No separate icon-only treatment inside the popout.

PDF endpoint implementation:
- Route: POST /convert/pdf
- Takes the already-converted HTML from the session/memory
- Passes it to weasyprint for PDF rendering
- Returns the PDF as a file download
- weasyprint requires system deps (Pango, Cairo, etc.)
- If weasyprint install fails on Render free tier, the PDF
  button shows "Coming soon" or is hidden. Do not block the
  rest of the Save popout on PDF availability.

---

## 7) Help Popout

Panel width: ~280px. Informational only -- no feedback here.

Contents:

a) About section:
   - "Decant makes web articles easier to read."
   - "It works best with articles, blog posts, and prose
     content."
   - "It does not handle JavaScript-heavy pages, login-required
     content, or interactive apps."
   - "Tip: If a page requires login, save it from your browser
     (File > Save As > HTML) and upload it here."

b) Note on URL-only features:
   - "Share and View Original are available when converting
     from a URL."

c) Future direction:
   - "Decant is currently focused on dyslexia. Support for
     other conditions including color vision differences is
     planned."

d) Links:
   - GitHub repo link
   - "Report an issue" link (GitHub issues)

---

## 7a) Inline Feedback Bar

Feedback is NOT in the toolbar. It appears as a thin bar
directly below the iframe after every conversion. This follows
the pattern used by Claude (thumbs on every response) --
low-friction feedback at the point of experience.

Layout: a single horizontal bar, visually lightweight.
- Left-aligned text: "How was this?"
- Thumbs up icon + Thumbs down icon
- On thumb click: optionally expand a small text field +
  submit button for detail. The thumb alone is a complete
  action -- text is optional.

Visibility:
- Hidden before conversion (no iframe content = nothing to rate)
- Visible after every conversion (URL or file upload)
- Resets on new conversion

Backend:
- POST /feedback
- JSON payload: { url_or_filename, rating, text, timestamp }
- Log to stdout as structured JSON. No database for v1.

---

## 8) Theme Token Definitions

The THEMES object expands from 4 content tokens to include
chrome tokens. All visual differentiation goes through CSS
variables set on the body element. Theme switching swaps a
class on body (e.g. body.light, body.sepia, body.dark,
body.contrast).

### Content tokens (existing, applied to iframe via CSS injection)
- --content-bg
- --content-text
- --content-link
- --content-visited

### Chrome tokens (new, applied to toolbar and popouts via body class)
- --toolbar-bg
- --toolbar-border
- --toolbar-shadow
- --toolbar-button-border
- --toolbar-button-hover
- --toolbar-button-active
- --icon-fill
- --popup-bg
- --popup-border
- --popup-shadow
- --popup-text
- --tooltip-bg
- --tooltip-text

### Token values per theme

LIGHT:
  --toolbar-bg: #ffffff
  --toolbar-border: rgba(12, 12, 13, 0.2)
  --toolbar-shadow: rgba(12, 12, 13, 0.1)
  --toolbar-button-border: transparent
  --toolbar-button-hover: rgba(12, 12, 13, 0.1)
  --toolbar-button-active: rgba(12, 12, 13, 0.15)
  --icon-fill: rgb(91, 91, 102)
  --popup-bg: #ffffff
  --popup-border: rgba(0, 0, 0, 0.12)
  --popup-shadow: rgba(49, 49, 49, 0.3)
  --popup-text: #1a1a1a
  --tooltip-bg: rgb(207, 207, 216)
  --tooltip-text: rgb(91, 91, 102)

SEPIA:
  --toolbar-bg: #f4ecd8
  --toolbar-border: rgb(91, 70, 54)
  --toolbar-shadow: rgba(91, 70, 54, 0.15)
  --toolbar-button-border: transparent
  --toolbar-button-hover: rgba(91, 70, 54, 0.1)
  --toolbar-button-active: rgba(91, 70, 54, 0.15)
  --icon-fill: rgb(91, 70, 54)
  --popup-bg: #f4ecd8
  --popup-border: rgba(91, 70, 54, 0.3)
  --popup-shadow: rgba(91, 70, 54, 0.2)
  --popup-text: rgb(91, 70, 54)
  --tooltip-bg: rgba(91, 70, 54, 0.15)
  --tooltip-text: rgb(91, 70, 54)

DARK:
  --toolbar-bg: rgb(66, 65, 77)
  --toolbar-border: rgba(249, 249, 250, 0.2)
  --toolbar-shadow: rgba(0, 0, 0, 0.5)
  --toolbar-button-border: transparent
  --toolbar-button-hover: rgb(82, 82, 94)
  --toolbar-button-active: rgb(91, 91, 102)
  --icon-fill: rgb(251, 251, 254)
  --popup-bg: rgb(66, 65, 77)
  --popup-border: rgba(255, 255, 255, 0.2)
  --popup-shadow: rgba(0, 0, 0, 0.5)
  --popup-text: rgb(251, 251, 254)
  --tooltip-bg: rgb(82, 82, 94)
  --tooltip-text: rgb(251, 251, 254)

CONTRAST:
  --toolbar-bg: #000000
  --toolbar-border: #ffee32
  --toolbar-shadow: rgba(0, 0, 0, 0.8)
  --toolbar-button-border: transparent
  --toolbar-button-hover: rgba(255, 238, 50, 0.1)
  --toolbar-button-active: rgba(255, 238, 50, 0.2)
  --icon-fill: #ffee32
  --popup-bg: #1a1a1a
  --popup-border: #ffee32
  --popup-shadow: rgba(0, 0, 0, 0.8)
  --popup-text: #ffffff
  --tooltip-bg: #1a1a1a
  --tooltip-text: #ffee32

---

## 9) Theme Switching Mechanism

Pattern: body class swap. No inline styles on chrome elements.

JS:
- On theme change, remove the previous theme class from body
  (e.g. body.classList.remove("dark"))
- Add the new theme class (e.g. body.classList.add("sepia"))
- Continue to inject content CSS into the iframe via
  buildOverrideCSS (content tokens only)
- Chrome tokens are picked up automatically via CSS variable
  inheritance from the body class

CSS:
- Define chrome variables on body (default = light values)
- Override per theme class:
  body.sepia { --toolbar-bg: #f4ecd8; ... }
  body.dark  { --toolbar-bg: rgb(66,65,77); ... }
  body.contrast { --toolbar-bg: #000000; ... }

Transition:
- Add after page load: body.loaded { transition: color 0.4s,
  background-color 0.4s; }
- This gives a smooth theme switch without flash on initial load.

localStorage:
- Theme key stays the same. Body class is set on page load
  from stored value.

---

## 10) Dropdown Open/Close Mechanism

Pattern: .open class on the parent <ul>.dropdown element.

JS:
- Click on .dropdown-toggle adds .open to its parent <ul>
- If another dropdown is already open, close it first
  (only one open at a time)
- Click outside any dropdown closes all
- Escape key closes the open dropdown

CSS:
```
.dropdown-popup {
  position: absolute;
  inset-inline-start: 48px;  /* toolbar width + padding + gap */
  z-index: 1000;
  background-color: var(--popup-bg);
  color: var(--popup-text);
  visibility: hidden;
  border-radius: 8px;
  border: 1px solid var(--popup-border);
  box-shadow: 0 0 10px 0 var(--popup-shadow);
}

.open > .dropdown-popup {
  visibility: visible;
}
```

When a dropdown is open, the toolbar border and shadow
become transparent (the popout visually "extends" from the
toolbar):
```
.dropdown-open .toolbar {
  border-color: transparent;
  box-shadow: 0 2px 8px transparent;
}
```

---

## 11) Tooltips

Each toolbar button has a <span class="hover-label"> child.
Positioned to the right of the button. Hidden by default,
visible on hover.

```
.hover-label {
  position: absolute;
  inset-inline-start: 40px;
  top: 50%;
  transform: translateY(-50%);
  white-space: nowrap;
  background-color: var(--tooltip-bg);
  color: var(--tooltip-text);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 13px;
  visibility: hidden;
  pointer-events: none;
  z-index: 1001;
}

.toolbar-button:hover > .hover-label {
  visibility: visible;
}

/* Suppress tooltip when dropdown is open */
.open > li > .dropdown-toggle:hover > .hover-label {
  visibility: hidden;
}
```

---

## 12) Visibility Rules

Share button and View Original button are hidden when the
conversion source is a file upload.

Implementation:
- After conversion, set a data attribute on a parent element:
  data-source="url" or data-source="file"
- CSS:
  [data-source="file"] .share-button,
  [data-source="file"] .view-original-button { display: none; }
- On new conversion, update the data attribute.

The toolbar strip shows 4 icons (file upload) or 6 icons
(URL conversion). The strip height adjusts naturally.

---

## 13) Icons

Use inline SVG or SVG as CSS background-image for each button.
Prefer inline SVG for theme colorability (fill inherits from
--icon-fill via currentColor).

Icon sources: Use simple, recognizable icons. Lucide or similar
open-source icon set. Do not use Font Awesome (license weight).

Icon mapping:
- Aa: text/typography icon (or literal "Aa" text)
- Theme: paint bucket or palette icon (FF uses a theme swatch)
- Save: download/arrow-down icon
- Share: share/link icon
- View Original: external-link icon
- Help: question-mark-circle icon

---

## 14) What to Remove

The current implementation has:
- #settings-panel (right-side slide-out)
- #settings-btn (gear icon in header or result bar)
- Related CSS for panel slide, margin-right shift on content
- View Original pill button in the result-bar

All of these are replaced by the toolbar. Remove:
- The settings panel HTML
- The settings button
- All CSS for panel slide-in/out and content margin shift
- The View Original pill button (moves into toolbar)
- The result-bar element (if it only contained View Original)

Preserve:
- All buildOverrideCSS logic
- All localStorage read/write logic
- All iframe CSS injection logic
- The applySettings function (refactor to work with new
  control elements but keep the same behavior)
- The THEMES content tokens (bg, text, link, visited) for
  iframe injection
- Font size zoom + width compensation coupling

---

## 15) Backend Endpoints (new)

### POST /convert/pdf
- Accepts: the converted HTML (from session or re-convert)
- Returns: PDF file (Content-Disposition: attachment)
- Implementation: weasyprint
- If weasyprint is unavailable, return 501 with message

### POST /feedback
- Accepts: JSON { url_or_filename, rating, text, timestamp }
- Returns: 200 OK
- Implementation: log to stdout as structured JSON
- No database. Logs are the storage layer for v1.

---

## 16) Implementation Chunks

### Chunk 4a: Toolbar skeleton + positioning
- Create toolbar HTML structure in index.html
- CSS for toolbar-container, toolbar, toolbar-button
- Position toolbar to left of content area
- No popout content yet -- just the 6 icon buttons
- Tooltips on hover
- Remove old settings panel HTML and CSS
- Remove old settings button
- Commit and push

### Chunk 4b: Text controls popout
- Move font/size/width/spacing controls into text-controls
  popout panel
- Wire up existing settings logic to new control elements
- Dropdown open/close mechanism (JS)
- localStorage persistence (same keys, same behavior)
- buildOverrideCSS and iframe injection (unchanged logic)
- Reset to defaults button
- Test all text controls work as before
- Commit and push

### Chunk 4c: Theme picker popout
- Theme grid in theme-controls popout
- Body class swap for chrome theming
- CSS variable definitions for all 4 themes
- Iframe content theming via buildOverrideCSS (existing)
- Theme transition on body.loaded
- localStorage theme persistence
- Test all 4 themes on toolbar + content
- Commit and push

### Chunk 4d: Save popout + endpoints
- Print / Download HTML / Download PDF buttons in popout
- Print: window.print() or iframe print
- Download HTML: serve as file attachment
- Download PDF: POST /convert/pdf with weasyprint
  (if weasyprint unavailable on Render, hide PDF button
  or show "Coming soon")
- Commit and push

### Chunk 4e: Share + View Original + visibility
- Share button: copy URL to clipboard, show confirmation toast
- View Original button: open source URL in new tab
- data-source attribute for URL vs file upload
- CSS visibility rules (hide share + view original for files)
- Commit and push

### Chunk 5: Help popout + inline feedback bar
- Help popout content (about text, URL-only features note,
  future direction note, repo and issues links)
- Inline feedback bar below iframe (not in toolbar)
- Thumbs up/down, optional text expand on click
- POST /feedback endpoint
- Feedback bar visible after conversion, hidden before
- Commit and push

### Chunk 6: PDF endpoint + monitoring/ops
- weasyprint integration (if not done in 4d)
- Sentry integration
- UptimeRobot or similar
- Structured logging cleanup
- Commit and push

---

## 17) Session Rules Reminder

These apply to ALL chunks. Sonnet must follow them.

1. Before modifying any file, read it first and confirm you
   understand the current state.
2. Fix ONE thing at a time, test, confirm, then move on.
3. Every chunk prompt ends with "commit and push."
4. Wait for Render deploy before pushing the next commit.
5. Never write fix prompts from assumptions -- diagnostic first.
6. Do not modify engine code (flowdoc/ directory).

---

## 18) Files Affected

- surface/templates/index.html -- major rewrite (toolbar HTML)
- surface/static/app.css -- major rewrite (toolbar CSS, theme
  variables, remove panel CSS)
- surface/static/app.js -- significant refactor (dropdown logic,
  theme class swap, rewire settings to new controls, save/share
  actions, feedback endpoint)
- surface/app.py -- add /convert/pdf and /feedback routes

---

## 19) Conflicts and Dependencies

- This spec supersedes the settings panel design in
  docs/surface-spec.md sections 5, 6, 7. Those sections
  describe the old slide-out panel and header bar layout.
  Update surface-spec.md during Task 8 (docs review).

- The View Original pill button (Chunk 3, Bug 4 fix) is
  removed and replaced by a toolbar button. The temporary
  placement note in the handoff doc is resolved.

- The "chrome stays neutral" decision from Chunk 3 is reversed.
  Chrome now participates in themes. The .dark-bg fix approach
  noted in the handoff doc is superseded by the CSS variable
  architecture in this spec.

- The current settings panel code (HTML, CSS, JS) is deleted,
  not incrementally modified. This is a replacement, not a
  refactor.

- No engine changes. The buildOverrideCSS function and iframe
  CSS injection pattern are preserved.
