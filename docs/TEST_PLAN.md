# Test and quality plan — TextMarker v0.1

## Automated checks (pytest)

### Term lists
- TXT/MD/CSV imports; BOM; UTF-8; CRLF and LF.
- Semicolon and comma CSV; quoted phrases containing separators.
- Blank and comment lines, disabled terms, duplicate terms, category colors and explicit colors.
- Unknown columns, missing expression, invalid boolean/color and empty list: clear behavior/errors.
- Danish letters, Unicode case folding and mixed-case text.

### Matcher
- Whole-word checks: `han` must not match `hans`.
- Phrases with spaces and tabs, punctuation and start/end of paragraph.
- Overlapping phrases: longest wins; equal-length tie by list order.
- Count accepted spans only; repeated matches, zero matches.
- Never match across paragraphs.
- Decomposed Unicode: safe explicit behavior without changing original text.

### DOCX integration
- A phrase split between `w:r` elements and between `w:t` nodes.
- Match starts/ends mid-run, bold/italic style boundaries and Word highlight inheritance.
- Normal and nested tables; headings, lists and page-break runs.
- Existing highlighting outside span unchanged.
- Non-text run children, bookmarks, hyperlinks, field instructions, drawings and tracked changes preserved or safely excluded.
- Header/footer, footnote/textbox excluded but retained.
- Compare text in every supported paragraph before and after, inspect `w:highlight` values and absence of new `w:strike`.
- Validate OOXML package; Word/LibreOffice opening smoke check where available; never claim a Word smoke test unless actually run.

### Output and safety
- Original source byte-identical before/after.
- Attempt to set output equal to source fails before writing.
- Atomic write on failure/cancellation: no partial output.
- CSV counts consistent with applied highlight spans; escaping of commas and newlines.
- No source text logged; no network.

### GUI / FSM
- State transition table and illegal-event rejection.
- Missing inputs and invalid paths, invalid terms, disabled Start state.
- Worker does not freeze UI; cancellation and error recovery.
- End-to-end smoke test on Windows; screenshots if possible.

## Performance and exit gates

Use synthetic 10k, 100k and 150k-word DOCX test manuscripts with many terms. Record Windows version, CPU, RAM, elapsed time and peak memory. No ungrounded speed claims.

Gate 1: parsing and matcher tests green.
Gate 2: DOCX fidelity and safety tests green.
Gate 3: GUI state and output consistency tests green.
Gate 4: Windows EXE build green, standalone smoke test evidenced.
Gate 5: Draft PR reviewed. No main merge or release without explicit approval.

## Required test report

Include total passed/failed/skipped, known unsupported Word constructs, sample document size and runtime, EXE SHA-256 and download location if a binary has been produced.
