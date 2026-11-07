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
- Commit: pending documentation commit below.
- Tests: 23 passed, including three launcher routes and legacy-window isolation smoke.
- Behavior: `text_tools_gui_entry.py` opens a Danish home screen; Text Marker and Risk Scanner use their existing windows; Word Index has an isolated placeholder route until Phase C; closing a module returns the user to the launcher.
- Next: Word Index service, stopword resources, exporters and GUI.
