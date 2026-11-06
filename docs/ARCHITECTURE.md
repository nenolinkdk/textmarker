# Architecture — TextMarker v0.1

## Layers

```text
PySide6 GUI (presentation only)
    | commands / state projection
Application controller + authoritative FSM
    | dependency-injected services
Input adapters (DOCX/TXT, CSV/TXT/MD)
    -> normalized TermSpec list
Matching engine (pure functions, paragraph offsets)
    -> non-overlapping MatchSpan list
DOCX highlight engine (OOXML run-aware transformations)
    -> output DOCX
CSV report writer + safe file writer
```

Use `src/textmarker/` with packages `ui`, `application`, `input`, `matching`, `docx`, `reporting`, `core`. Keep GUI event callbacks as commands; they must not independently own processing state.

## FSM

States: `IDLE`, `FILES_READY`, `VALIDATING`, `READY`, `PROCESSING`, `COMPLETED`, `FAILED`, `CANCELLED`.

Events: `SET_SOURCE`, `SET_LIST`, `VALIDATE`, `VALIDATION_OK`, `VALIDATION_FAIL`, `START`, `PROGRESS`, `COMPLETE`, `FAIL`, `CANCEL`, `RESET`.

Core transitions:

| From | Event | To |
|---|---|---|
| IDLE | Both paths supplied | FILES_READY |
| FILES_READY | VALIDATE | VALIDATING |
| VALIDATING | VALIDATION_OK | READY |
| VALIDATING | VALIDATION_FAIL | FAILED |
| READY | START | PROCESSING |
| PROCESSING | PROGRESS | PROCESSING |
| PROCESSING | COMPLETE | COMPLETED |
| PROCESSING | FAIL | FAILED |
| PROCESSING | CANCEL | CANCELLED |
| COMPLETED / FAILED / CANCELLED | RESET | IDLE |

Path or option changes invalidate previous validation. `PROCESSING` must use a worker thread or equivalent, with marshalled GUI updates. Cancellation is cooperative; do not leave an incomplete output file.

## Data contracts

`TermSpec(expression: str, category: str, highlight_color: str, enabled: bool, ordinal: int)`

`MatchSpan(start: int, end: int, term_id: int)` where offsets refer to original visible paragraph text and `[start,end)` interval semantics. Matching engine must distinguish raw paragraph text offsets from its normalized search representation.

`DocumentSummary(word_count: int, expression_count: int, applied_matches: int, warning_count: int)`

`ProcessingWarning(location: str, code: str, message: str)`

## DOCX algorithm

1. Open DOCX as a ZIP/OOXML package via python-docx/lxml, enumerate supported stories in document order.
2. Extract visible paragraph text from eligible `w:t` nodes while retaining a mapping from each codepoint offset to run/text-node positions. Do not flatten hyperlinks, tracked changes or field-like markup unless preservation and mapping are proven.
3. Search with a Unicode-aware literal multi-term engine and build candidate spans. Resolve overlaps deterministically.
4. Translate chosen spans back to XML text nodes/runs. Split affected text runs at exact boundaries, carrying run properties forward; preserve whitespace via `xml:space="preserve"`. Add/replace `w:highlight w:val="..."` only within matching pieces.
5. Write a new package and validate text equality plus expected highlights. Save to a temporary sibling path and atomically move to output target after success.

Strict safety invariant: keep the original DOCX's nontext content, relationships and structure. For unsupported XML runs, skip and warn instead of applying unsafe mutations. Acceptable run splitting must retain all semantic run attributes. Consider implementing at the OOXML level rather than relying solely on python-docx run.text assignment, which can lose special children.

## Highlight palette (v0.1)

Explicitly map UI/CSV labels to Word OOXML values: `yellow`, `green`, `cyan`, `magenta`, `red`, `blue`, `darkYellow`, `darkGreen`, `darkCyan`, `darkMagenta`, `darkRed`, `darkBlue`, `darkGray`, `lightGray`, `black`, `white`. Prefer readable palette choices in GUI and warn about dark highlight readability. The Word UI may display localized color names.

## Risks and mitigation

- Run boundaries and mixed styles: span-to-node map + regression fixtures.
- OOXML fields/hyperlinks/track changes: explicit unsafe-region exclusions.
- Unusual documents: fail closed with warnings, never corrupt.
- Unicode offsets: preserve original offsets and compare before/after.
- Scale: compile term matching structures once, avoid O(terms × full-document-length) if performance becomes a problem.
- ZIP bombs and huge XML: validate document size, archive entry sizes and parsing limits before processing.

## Planned layout

```text
src/textmarker/
  __main__.py
  application/controller.py
  application/fsm.py
  core/models.py
  input/terms.py
  input/source.py
  matching/matcher.py
  docx/highlighter.py
  reporting/csv_report.py
  ui/main_window.py
tests/unit/
tests/integration/
tests/fixtures/
examples/terms.csv
docs/
.github/workflows/
```
