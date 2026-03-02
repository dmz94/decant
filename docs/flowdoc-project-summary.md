# Flowdoc Project Summary

*Context for Strategic Review -- March 2026*

---

## 1. Origin

Flowdoc started with a specific, personal problem: converting a recipe PDF into a format that was easier for a dyslexic family member to read. Manual reformatting in PDF-XChange Editor with dyslexia-friendly typography (including OpenDyslexic) worked, but was slow, repetitive, and fragile. The insight came when the same recipe content turned out to be available as HTML.

HTML already contains structure -- headings, paragraphs, lists. If you can rely on semantic structure, you can build a tool that re-renders content for readability without solving the much harder problem of inferring structure from fixed-layout formats. This mapped directly to prior professional experience: years at Oxford University Press building systems that ingest structured content (XML/JSON) and re-emit it in different forms. The pattern is parse, model, render -- and it applies here.

## 2. Initial v1 Design

v1 was scoped intentionally narrow: semantic HTML in, self-contained readable HTML out. The architecture was modeled as a compiler pipeline -- extract main content, sanitize, parse into an explicit internal model (IR), then render from the model only. Key properties: deterministic output (same input + version + flags = byte-identical result), strict security boundary (sanitize before parse), and explicit failure modes (reject non-semantic HTML rather than guess).

The tech stack locked early: Python 3.12+, BeautifulSoup with lxml for tolerant parsing, nh3 for sanitization, and a deterministic fallback content selector (main > article > body). Typography defaults followed British Dyslexia Association guidelines: sans-serif fonts, 18px body text, 1.5 line-height, 60-70 character line length, left-aligned, off-white background. OpenDyslexic was included as an optional toggle, not a default -- the research does not support universal efficacy claims.

The strategic framing positioned Flowdoc as infrastructure, not a consumer app. The differentiator versus browser Reader Mode was portability (self-contained file), determinism (CI/audit-friendly), and embeddability (server-side, no browser required). Primary adoption target: institutional integrators (publishers, educational platforms, compliance teams).

## 3. What Broke During Real-World Validation

The deterministic content selector (main > article > body) failed on real-world websites. Pages from major sites carried navigation menus, footers, and site chrome into the extracted content because the selector had no ability to distinguish main article content from boilerplate. The assumption that semantic HTML would arrive clean was wrong for the web-sourced use case.

This forced integration of Trafilatura as the primary content extraction engine, with the original deterministic selector retained as a fallback for clean developer HTML. Trafilatura resolved the boilerplate problem but introduced its own set of limitations: trailing CMS footer patterns leaking through on some sites (Cleveland Clinic, WikiHow), inline code tags promoted to block-level pre elements (fragmenting sentences), dropped spaces at inline element boundaries, duplicate list items from flattened nested lists, and Wikipedia lead section fragmentation where dense link-heavy paragraphs broke into single-phrase fragments.

Visual validation against a fixture corpus (Wikipedia, NHS, BBC Good Food, MDN, and others) surfaced these issues systematically. Some were simple bugs (empty paragraphs), but others were fundamental Trafilatura behaviors that could not be fixed without risky heuristics. MDN reference table pages failed entirely because their content lives in tables, which Flowdoc strips by design -- wrong input type, not a bug. Recipe sites lost heading structure during extraction, causing validation failure.

## 4. What Changed in Response

Technically, the pipeline gained a dual-mode architecture: "transform mode" for clean developer HTML (using the deterministic fallback) and "extract mode" for real-world web pages (using Trafilatura). Extraction mode measurement confirmed the baseline Trafilatura configuration (favor_precision=True, no_fallback=False) was optimal -- a recall-oriented mode performed significantly worse on the test corpus, extracting less content from three fixtures (Eater, ProPublica, PBS) by hundreds of thousands of characters.

Strategically, the project sharpened its identity. The positioning moved from "dyslexia-friendly converter" to "accessibility document compiler for prose content" -- infrastructure that enables institutions to reliably produce accessible reading versions at scale. The scope boundary became explicit: article-like prose documents only. Table-heavy reference content, recipe sites, and JS-rendered SPAs are rejected, not handled poorly.

Documentation was reorganized significantly. The original planning documents had grown unwieldy with role confusion and duplication across files. A restructuring reduced documentation from over 2,800 lines to approximately 1,300 while establishing a clear hierarchy: strategy.md as the canonical identity document, decisions.md as the authoritative implementation spec, and architecture.md for locked technical choices. Known limitations were documented explicitly as boundaries rather than bugs.

## 5. Strategic Identity Options

Four candidate identities have been articulated through strategy documents and external analysis. None has been validated with real demand signals. The choice determines audience, distribution, monetization, and scope -- making it the central open question for the project.

**Identity A: Infrastructure Accessibility Compiler.** Flowdoc as embeddable pipeline infrastructure for institutions -- publishers, universities, LMS platforms, compliance teams. The buyer is an engineering or accessibility lead integrating it into CI or publishing workflows. The value proposition is determinism, auditability, and reproducible accessible output at scale. This is the identity described in strategy.md. The risk is a cold-start problem: institutions are unlikely to adopt infrastructure for a workflow they have not formalized, and no institutional buyer has been identified or validated.

**Identity B: Consumer Dyslexia Reading Product.** Flowdoc as a direct-to-reader tool -- browser extension, web app, or similar end-user-facing product. External analysis scored this poorly because the current architecture actively fights consumer UX (semantic HTML input constraints, no JavaScript support, no browser extension) and the competitive landscape includes well-funded incumbents (Immersive Reader, BeeLine Reader, Bionic Reading). The project's own documents explicitly reject this identity.

**Identity C: Developer Niche CLI Utility.** Flowdoc as a developer build tool, adopted bottom-up via pip install by docs-as-code teams or static site publishers. The accessibility focus narrows the developer audience, and the competitive moat against Readability.js plus custom CSS is shallow. Easy to ship and easy to try, but unclear path to sustained adoption or ecosystem-standard status.

**Identity D: Free Open-Source Community Tool.** Flowdoc as a practical, no-cost utility for parents, teachers, SEN coordinators, and accessibility practitioners -- the people who actually reformat documents today. Distribution through dyslexia communities and SEN networks rather than institutional sales or developer ecosystems. No monetization. Distinct from Identity B because it is not attempting to be a consumer product with acquisition funnels; it is a focused utility for a specific community. Distinct from Identity A because it does not depend on institutional buyers recognizing a problem they have not formalized.

## 6. What Remains Unresolved

The strategic identity question described above is the primary unresolved issue. All downstream decisions -- who the audience is, how Flowdoc is distributed, whether it generates revenue, and what scope expansion looks like -- depend on which identity is selected and validated.

Extraction quality is still dependent on Trafilatura's behavior. Trailing CMS boilerplate, inline code fragmentation, missing spaces at element boundaries, and Wikipedia lead section fragmentation are all documented as v1 known limitations deferred to v2. Trafilatura configuration parameters (favor_precision, fast, prune_xpath) and minimal deterministic heuristics (tail boilerplate trimmer, orphaned trailing section detector) have been identified as next steps but not yet implemented.

The core value proposition is unvalidated with real users. The planned comparison protocol (Flowdoc output vs. browser Reader Mode vs. original formatting, measured by reread frequency, line-loss incidents, and fatigue) has not yet been executed. Without this signal, any identity -- infrastructure, consumer, developer, or community -- lacks empirical grounding.

The internal Python library is not yet a stable public API, and the CLI remains the only supported integration surface. OpenDyslexic font embedding is specified but not implemented. Input validation, fixture corpus expansion, golden file testing, and determinism validation remain on the v1 completion checklist.
