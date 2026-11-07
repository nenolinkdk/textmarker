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

## Review follow-up

The scanner now distinguishes `categories=None` (all categories) from an explicit category set, rejects unknown categories, preserves filtered rule-to-finding mapping, rejects conflicting duplicates and malformed/extra CSV columns, requires non-empty categories, protects pre-existing DOCX/report files, atomically writes reports, removes only run-owned artifacts on cancellation, and exposes warnings through the summary model. The GUI uses a checked category list and treats cancellation as a normal result.

- Review-fix source commit: `8a4d93c6933dad59d10a107f292c2316dfe88a0d`
- Final artifact: `dist-risk-final/Nenolink-Translation-Risk-Scanner-0.1-TEST.exe`
- Build timestamp: 2026-11-07 10:54:32 local Windows time
- Size: 50,359,321 bytes
- SHA-256: `8CE8AB26B224220043C04E3F69555CC7364F16262EEC56678B42BEA24B447B69`
- Full pytest: 18 passed.
- Packaged GUI smoke: one visible window confirmed.

## RiskWorker follow-up

`RiskWorker` now calls the transaction exactly once, does not write the report a second time, and never deletes outputs after a committed transaction. It preflights DOCX, report and summary paths, returns the transaction result and paths to the GUI, and reports finding/warning counts. End-to-end worker tests exercise real DOCX/CSV inputs, successful creation of all three outputs, and cancellation with no outputs.

- Worker fix source commit: `1b3ac8dc1fe586c38117a2a961ff45972132b9c6`
- Final artifact: `dist-risk-worker/Nenolink-Translation-Risk-Scanner-0.1-TEST.exe`
- Build timestamp: 2026-11-07 11:16:24 local Windows time
- Size: 50,361,868 bytes
- SHA-256: `ABC14EA5E50FC684C97DDE26F96F848D405F319F47E7522206EC4ABD912A5D1F`
- Full pytest: 22 passed.
- Packaged GUI end-to-end: real DOCX and CSV scanned through the GUI; DOCX, occurrence report and summary report were created and readable.

## Transactional output follow-up

DOCX, occurrence CSV and optional summary CSV are now produced in same-directory temporary files. Final paths are reserved with exclusive create/no-replace semantics before publication; if report generation, cancellation, or concurrent destination creation fails, temporary files and only paths reserved by this run are removed. Pre-existing files are never overwritten or deleted. Fault-injection coverage includes report errors, cancellation between DOCX/report publication, concurrent creation and optional summaries.

- Transaction fix source commit: `88aa7dc594e0849c90bc554e94785c2846d4c396`
- Final artifact: `dist-risk-transactional/Nenolink-Translation-Risk-Scanner-0.1-TEST.exe`
- Build timestamp: 2026-11-07 11:01:02 local Windows time
- Size: 50,361,706 bytes
- SHA-256: `09747AD83CB899CE6B678E17DCC5E4E84A8814536966C80B6123FCA2AC5AA69`
- Full pytest: 20 passed.
- Packaged GUI smoke: one visible window confirmed.
