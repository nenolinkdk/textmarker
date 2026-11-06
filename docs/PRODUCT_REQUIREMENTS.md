# Product requirements — TextMarker v0.1

## Purpose

An editorial aid for authors, translators and reviewers who want to locate selected words and phrases in a long manuscript, e.g., a 100,000–150,000-word novel. The output is a separate Word document in which matched text has colored background highlighting.

## Scope and acceptance requirements

**Sources:** .docx and UTF-8 .txt. Output always .docx. Files stored locally. No cloud, no AI. Source file never modified or overwritten.

**Term lists:** UTF-8 .txt and .md with one literal term per line; ignore empty lines and lines beginning with `#`. Markdown headings and bullet items (`-`, `*`) may be stripped by a documented simple parser. For CSV, support columns `expression,category,color,enabled` (header required); optional category, color and enabled values. UTF-8 BOM, commas and semicolons, quoted fields; case-insensitive header names. Default highlight is yellow. Category colors can be configured in app; explicit per-term color overrides the category color. Unsupported colors are validation errors. Word highlight palette rather than arbitrary RGB in v0.1.

**Default options:** Case-insensitive and whole-words-only. Literal matching, not regular-expression syntax. Include occurrences of multiword expressions even across different runs within the same paragraph. Do not silently include substrings of longer words; e.g. `han` must not match inside `hans`. Unicode case folding includes Danish æ/ø/å. Use clearly documented handling for composed/decomposed Unicode forms; if full canonical equivalence cannot be mapped safely back to original offsets, avoid matching rather than editing source text.

**Whitespace:** Match an expression's internal spaces to one or more normal spaces or tabs inside the same paragraph; do not match across paragraph or line-break boundaries in v0.1. Preserve the source text exactly.

**Overlaps:** Prefer longest matching expression; if equal length, first term-list order. Applied spans must not overlap. Count only applied highlights, not discarded overlapping candidates. Deduplicate identical terms deterministically and warn about conflicts.

**DOCX:** Preserve the source's structure and existing formatting, including bold/italic, headings, lists, page breaks, tables and existing highlighting outside matches. Support body and table-cell paragraphs, including nested tables. Handle matches spanning adjacent text runs (different styles). Never reassemble a whole paragraph using plain text. Unsupported Word structures (fields, drawings, hyperlinks, tracked changes, footnotes, text boxes, etc.) must be preserved and not damaged; skip unsafe matching contexts and report limitations. In v0.1, headers/footers, comments, footnotes/endnotes and text boxes are not processed. Existing highlights inside an intended match can be overwritten by the selected highlight color, but outside matches must remain untouched.

**TXT:** Convert UTF-8 text to DOCX; preserve paragraph boundaries (blank lines remain blank paragraphs). TXT has no style to preserve.

**Output:** New filename suggested as `<source_stem>_marked.docx`; separate `<source_stem>_matches.csv`. Ask for save location. File writes should be atomic when feasible; never replace source input even if user selects same path. Report expression, category, color, applied_count and total_count, including zero matches. The meaning of total_count should be the sum of applied_count in the report. Display summary with document word count, expression count and applied-highlight count. Empty matches are valid.

**GUI:** Danish interface initially, with an architecture ready for localization. File pickers, input validation, checkbox for case sensitivity and whole-word matching, highlight color selection/default category colors, progress indicator, cancel where safely possible, summary/results and human-readable errors. UI must remain responsive for a 150,000-word manuscript.

**Performance:** Target 150,000 words on a typical Windows 11 workstation without freezing the UI; measure performance and memory in tests, but do not invent a timing SLA without hardware-based benchmarking.

## Out of scope

PDF/RTF input, direct editing of original files, automatically detecting stylistic weaknesses, inflectional/morphological matching, regex rules, language-model analysis, macros, and cloud synchronization.

## Nonfunctional requirements

- Windows 10/11 64-bit, standalone EXE without requiring Word installed for generation; opening the DOCX requires a compatible word processor.
- Deterministic output for fixed input/options (except normal DOCX zip timestamps and metadata).
- Clear diagnostic errors and partial-feature warnings, no silent data loss.
- No user content in logs by default and no network transmission.
- Lightweight packaging; no installation needed for TEST executable.
