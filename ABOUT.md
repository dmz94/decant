# About Flowdoc

Flowdoc started with a practical problem: converting a recipe PDF into a format that was easier for my dyslexic son to read.

I used PDF-XChange Editor to manually reformat the document with dyslexia-friendly typography (including OpenDyslexic). It worked, but it was slow, repetitive, and fragile. After doing that, I discovered the recipe site could export the same content as HTML.

That was the unlock: HTML already contains structure (headings, paragraphs, lists). If you can rely on semantic structure, you can build a tool that **re-renders content for readability** without solving the much harder problem of inferring structure from fixed-layout formats.

I've spent years building systems that ingest structured content and re-emit it in different forms. At Oxford University Press, I ran the technology team for the dictionary division. We stored data in structured formats (XML/JSON) and built parsers and renderers to extract, transform, and present content reliably. The same general approach applies here:

- parse structured input
- map it into a minimal internal model
- render to a stable, readable output

Although the trigger was a recipe, the underlying issue is broader. Articles, manuals, technical docs, educational materials, and work documents often have content that is "there," but presented in a way that creates unnecessary barriers for dyslexic readers.

Flowdoc is intentionally narrow in v1:
- input is semantic HTML only
- output is self-contained readable HTML
- readability over fidelity is the core principle
- validation is done with real dyslexic readers before expanding scope

If v1 proves value, later versions can add more inputs (Markdown, DOCX) and outputs (native PDF, DOCX), and potentially content transformations informed by writing-style guidance.
