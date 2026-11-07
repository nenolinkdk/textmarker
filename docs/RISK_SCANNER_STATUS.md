# Translation Risk Scanner v0.1 status

Implemented on `feature/translation-risk-scanner-v0.1`, based on `origin/feature/v0.1-mvp` at branch creation. Existing TextMarker tests and entry points remain unchanged.

## Verification

- Clean-build venv: Python 3.12.14 64-bit, PySide6/shiboken6 6.7.3, PyInstaller 6.11.1.
- Full pytest: 14 passed.
- Risk GUI smoke: passed; Danish window constructed with category filter, case and whole-word controls.
- Risk DOCX flow: passed; occurrence report contains one row per finding, output contains `w:highlight`, no `w:strike`, and source remains separate.
- Packaged risk GUI smoke: passed; one visible Windows window was confirmed with `IsWindowVisible=True`.

## Build

- Build source commit: `c113e97ac8b537686cbf2facd216a1a879dd9ae7`
- Artifact: `dist-risk/Nenolink-Translation-Risk-Scanner-0.1-TEST.exe`
- Build timestamp: 2026-11-07 10:46:54 local Windows time
- Size: 50,356,697 bytes
- SHA-256: `9B122E4CB8AF6A0A3EF70EE14E778B747189B6F78C658C61DA6213D38FD855D3`

## Limitations

Findings are literal lexical review flags, not translation-error judgments. Norwegian/Danish alignment, semantic equivalence, omission detection, rewriting, and intentional nonstandard character voice are out of scope. Unsupported OOXML paragraphs are skipped conservatively and require human review; locators use `body/p[n]` and are not Word bookmarks. Microsoft Word opening/repair-warning validation was not available.
