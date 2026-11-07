# v0.2 status

## Phase A — documentation

- Base: `origin/feature/translation-risk-scanner-v0.1`
- Branch: `feature/text-tools-v0.2`
- Status: design committed; implementation not started.
- Tests: inherited baseline not rerun in Phase A.
- CI: pending draft PR.
- Artifact: none.
- Next: shared launcher with three module routes.
- Outstanding: all implementation and Windows acceptance phases; Microsoft Word manual gate.

## Phase B — shared launcher

- Status: implemented and tested.
- Commit: `77fb67b48509f310caa2997ecf912615dbfe908d`.
- Tests: 23 passed, including three launcher routes and legacy-window isolation smoke.
- Behavior: `text_tools_gui_entry.py` opens a Danish home screen; Text Marker and Risk Scanner use their existing windows; closing a module returns the user to the launcher.
- Next: Word Index service, stopword resources, exporters and GUI.

## Phase C — Word Index

- Status: implemented locally; pending commit and PR update.
- Features: safe DOCX body/table paragraph extraction, Unicode NFC/casefold tokenization, Danish and Norwegian Bokmål modes, deterministic `A–Z, Æ, Ø, Å` ordering, exact 100-word editable stopword resources, CSV/TXT export, cancellation and paragraph progress.
- Safety: outputs use exclusive creation and never replace an existing file; cancellation writes no output.
- Tests: 27 passed locally with the repository virtual environment and offscreen Qt. The first run was blocked by a Windows TEMP ACL issue; rerun used a repository-local temporary directory.
- Limitation: unsupported OOXML run structures are skipped with warnings; no lemmatization is performed. Future language support is intended through the language/stopword boundary.
- Next: Phase D persistent local file inventory, then integration/build acceptance.
