# v0.1 implementation handoff

Implemented on `feature/v0.1-mvp` from `docs/v0.1-codex-handoff`.

## Completed

- Deterministic TXT/MD/CSV term parsing, including UTF-8 BOM, comma/semicolon CSV, duplicate suppression, enabled flags and explicit Word palette validation.
- Unicode NFC/case-folded literal matching, Danish letters, whole-word matching, flexible internal spaces/tabs, longest-match overlap resolution and stable term-order ties.
- OOXML DOCX marking for body paragraphs and table-cell paragraphs, including matches spanning runs. Marking adds `w:highlight` and never adds `w:strike`; output is atomic and never replaces the source.
- CSV report output and a local CLI entry point.
- Pytest configuration and Windows CI/build scripts.

## Verification in this environment

- Bundled Python 3.12.14 was available; `lxml 6.1.1` and `python-docx 1.2.0` imported successfully.
- Synthetic DOCX integration check: 3 matches applied across body/table content; output contained 3 `w:highlight` elements and 0 `w:strike` elements.
- Pytest could not run because pytest is not installed in the bundled runtime.
- PyInstaller/GUI smoke testing was not run because PySide6, PyInstaller and a configured system Python were unavailable.

## Known limitations

The PySide6 GUI, FSM worker/cancellation flow and regression coverage are now present. Hyperlinks, tracked changes, fields, drawings, headers/footers, footnotes/endnotes and text boxes are not processed. Microsoft Word opening was not available in this environment, so no Word repair-warning claim is made.

## Verification update

- Virtual environment: `.venv`, Python 3.12.14.
- Pytest: 12 passed, including GUI-option forwarding, FSM cancellation, cancellation cleanup, progress completion, full split-run coverage, unsafe-run preservation and Unicode offset safety.
- Headless GUI smoke test: passed.
- Synthetic 150,000-word matcher: 56,250 matches, 1.587 seconds, 18,756,502 peak traced bytes.
- Windows executable: `dist/TextMarker-0.1-TEST.exe`, 67,214,355 bytes, SHA-256 `6388C82B7074ABF5A0EF7DF795E4A6F5BCB0325A347C61C36BD35D996C4DBD87`.
- EXE smoke test: launched and remained alive for five seconds.
- Microsoft Word was unavailable; no Word opening/repair-warning result is claimed.
- Draft PR: https://github.com/nenolinkdk/textmarker/pull/2

## Review follow-up

The review fixes now cover complete highlighting across every safe run in a phrase, fail-closed handling for runs containing breaks/drawings/multiple text nodes, conservative Unicode offset handling, cooperative cancellation before package output, save-dialog output selection and source overwrite protection.

Final stabilization additionally forwards case-sensitive/whole-word settings from the GUI, treats cancellation as a normal workflow terminal state, removes both DOCX and CSV artifacts on cancellation, reports paragraph-based percentage progress, and documents that paragraphs containing ambiguous Unicode expansions are skipped conservatively without offset-unsafe edits.
