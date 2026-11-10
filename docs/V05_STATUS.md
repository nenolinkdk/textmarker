# Nenolink Text Tools v0.5 status

## Phase B — terminology data model and persistence

- Branch: `feature/text-tools-v0.5`
- Phase A: `3b178ad5f2da485a48bfee94bfe14543d566450f`
- Phase B implementation: pending commit
- Schema version: **2**
- Automated suite: **55 passed, 0 failed**

Implemented: Qt-independent SQLite terminology repository, normalized BCP 47 tags, concept/term CRUD, multilingual terms, explicit statuses, sources, client/project associations, deterministic search/filtering, possible-duplicate detection, foreign keys, transactions, integrity checks, v1→v2 migration with backup, unsupported-newer-schema rejection and backup API.

Not implemented by design: GUI, CSV import/export, TBX, TMX, XLIFF, Prompt Builder, scanner projection and AI integration.

Known limitation: migration backups are retained beside the database and are not automatically rotated. Scanner integration has only a read-only `TerminologyProjection` boundary; no terminology record can affect existing scans.

## Phase C — terminology GUI and CSV

- Terminology workspace added to AppShell and uses the Phase B SQLite repository as its sole storage.
- GUI supports concept browsing/search, multilingual terms, status editing, definitions, subject fields, deletion confirmation and CSV import/export.
- CSV supports UTF-8/BOM, comma/semicolon delimiters, quoted fields, deterministic canonical export, filter export and overwrite protection.
- Automated suite: **59 passed, 0 failed**.
- Remaining limitation: the GUI import action currently auto-maps canonical headers; a full interactive customer-column mapping/profile dialog and row-by-row preview is still outstanding.

## Phase C completion

- Terminology route is available from AppShell and backed by `TerminologyRepository`.
- Canonical CSV preview/import/export is implemented with validation, transaction rollback and no-overwrite export.
- Complete suite: **59 passed, 0 failed**.
- Windows TEST EXE built successfully; the packaged process was started and remained responsive. GUI route verification is automated; direct packaged click-through of the Terminology page remains limited by the current desktop automation session.

## Phase C2 — module introductions and guided mapping

- Added reusable `ModuleIntroduction` metadata component for all 12 navigation items.
- Added stable help IDs and offline `docs/manual/help.html` anchors, bundled by PyInstaller.
- Added centralized `0.5.0` version definition used by the application title.
- Added interactive CSV mapping dialog with language selection and validation, plus local mapping-profile persistence API.
- Complete suite: **61 passed, 0 failed**.
- Packaged build completed; process started responsive. Direct packaged click-through of the mapping dialog remains pending in this desktop session.

## Phase D — Prompt Builder

- Added Qt-independent deterministic FSM with explicit states, guards, Back, Reset, Edit and Save transitions.
- Added local PromptStore CRUD, search, duplicate and text export, with six initial review templates.
- Added Prompt Builder window in the Prompt Library route with task/language/domain/criteria/output steps, editable preview, clipboard copy and local save/reopen.
- Complete suite: **65 passed, 0 failed**.
- Final packaged build completed; the executable process started and remained responsive. Full wizard click-through remains pending in the current desktop session.

## Phase E — complete user experience

- Added two connected prose paragraphs for each of the 12 module introductions in all six locale resources, while retaining structured INPUT/OUTPUT/USE/WORKFLOW sections.
- Added Prompt Builder help anchor and documentation for templates, editing, saving, reopening, copying, confidentiality and limitations.
- Added generated concept-ID option to guided CSV import; explicit mapping remains required for term and language, and concepts are never silently merged.
- Added regression coverage: **67 passed, 0 failed**.
- Final packaged GUI click-through remains limited by the desktop session; startup is verified after the final build.

## Phase F — final GUI completion and Windows acceptance

- Added GUI mapping-profile save, select, compatibility validation and delete controls.
- Added explicit generated concept-ID import option and bundled DA-interference CSV example using the actual supported schema.
- Added linguistic-purpose prose and scanner/rule documentation anchors.
- Final automated suite: **68 passed, 0 failed**.
- Acceptance matrix: `V05_PHASE_F_ACCEPTANCE.md`.

## Phase G — release candidate acceptance

- Baseline verified on `feature/text-tools-v0.5`, local HEAD `cb311617928e83e7644ec392d2aa7b6e2dfec169` before Phase G changes.
- Complete automated suite: **68 passed, 0 failed** (one PytestCacheWarning due to cache permissions).
- Actual parser audit completed for Translation Risk, DA-interference and canonical v0.4 rule packs. Documentation now distinguishes their schemas and includes `interference.rules` and `tutorial.overview` anchors.
- Push was attempted and blocked by network connectivity; the exact error is recorded in the Phase G acceptance report. Remote synchronization is not claimed.
- Packaged startup can be verified, but full packaged GUI click-through and Microsoft Word visual acceptance remain pending in this desktop session.
- New RC artifact: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 51,943,095 bytes, SHA-256 `DE5B5B1DFB3904B0D8F8A0A0FACCC6B9DD61FDA7E08A2BAE5487F1B5DF98F22C`; built from `830f4118e90d89e7ea0a84a16d4d316d63e26403`; separate-process startup remained responsive.
- Added the documentation coverage matrix in `V05_DOCUMENTATION_COVERAGE.md`. Danish and English now have module-specific linguistic input→processing→output prose; the four other locales remain flagged for native linguistic review.
- Rebuilt the v0.5 TEST executable from `2cc8a5a07d4305408697496a6256a412c5ce5a6d`: 51,947,631 bytes, SHA-256 `41266E96BDA8376F28090ED60A200262121B95F16FD87C78757B3B24072D065E`; separate-process startup remained responsive.
- Phase H added `V05_PHASE_H_WINDOWS_CHECKLIST.md` and expanded the three rule-schema procedures. Since the current HEAD is newer than the previous RC build, a fresh build is required for final provenance.
- Phase H RC build from `b3e930253a0b5951e98194f724a1b3cacb4899c`: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 51,947,979 bytes, SHA-256 `FE3D862F16FE2B0A2BA21DBF81352469C0D5E3FF190C525AA5A7EA6D1A4E0ACE`; separate-process startup remained responsive.
