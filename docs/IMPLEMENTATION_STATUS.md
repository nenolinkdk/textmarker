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

No draft PR was created because this environment could not authenticate to GitHub (`gh` is present but network access to GitHub was unavailable). The branch is ready for push and draft-PR creation by an authenticated developer.
