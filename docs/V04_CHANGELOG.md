# v0.4 changelog

## Phase A

- Dokumenteret multilingual foundation, AppShell, localization, rule schema, project format, testplan og beslutninger.

## Phase B

- Tilføjet registry for `da`, `sv`, `nb`, `en`, `de`, `fr`.
- Tilføjet locale resources, engelsk fallback og missing-key detection.
- Tilføjet validerede JSON project profiles med atomic persistence.
- Tilføjet canonical rule/finding models, v0.2/v0.3 adapters og pipeline interfaces.
- Complete suite: 38 passed.

## Phase C

- Tilføjet AppShell med venstre navigation, central workspace og collapsible contextual help-panel.
- Tilføjet Settings med UI/source/target language selectors og local project profile persistence.
- Legacy module windows åbnes via adapters; processing behavior og File Inventory storage er bevaret.
- Phase C suite: 39 passed.

## Phase D

- Tilføjet lokal RulePackStore med canonical CSV persistence, legacy adapters og duplicate protection.
- Tilføjet Glossaries & Rules workspace med import, search og rule table.
- Tilføjet lokal Prompt Library med seks templates og custom prompt save.
- Ingen external AI API, cloud upload eller TBX.
- Phase D suite: 42 passed.

## Phase F

- Added deterministic multi-pack merging with duplicate/conflict rejection.
- Added project rule-pack selection and persistent association controls.
- Complete suite: 44 passed before Windows build.

## Phase F

- Built `Nenolink-Text-Tools-0.4-TEST.exe` from Python 3.12/PyInstaller 6.11.1.
- Microsoft Word manual acceptance remains pending.

## Phase E

- Added exact v0.2/v0.3/v0.4 CSV schema detection; ambiguous headers are rejected.
- Added persistent rule enable/disable/remove operations and project active-pack validation.
- Added explicit DA scanner integration adapter with language-pair checks.
- Complete suite: 43 passed.

## P0 hotfix

- Added explicit PyInstaller data inclusion for `textmarker/multilingual/locales`.
- Added source/package/frozen resource lookup and controlled missing-locale errors.
- Fixed packaged AppShell Settings navigation mapping.
- Verification: 46 tests passed; fresh `Nenolink-Text-Tools-0.4-TEST-hotfix.exe` launched successfully.

## v0.4.1 Phase A

- Added the v0.4.1 specification, architecture, implementation plan and decision log.
- Defined persistent UI-language preferences, localized guidance/manual architecture, first-run tutorial FSM, future Prompt Builder FSM, Terminology concepts and interoperability evaluation boundaries.
- No application behavior was changed in Phase A.

## v0.4.1 Phase B

- Verified 46 automated tests and the existing packaged startup/resource-loading hotfix.
- Recorded the missing packaged project-workflow GUI controls as an integration blocker.
- No application code or EXE was changed because no baseline defect was reproduced.

## v0.4.1 Phase C

- Added persistent synchronized UI-language selectors in AppShell and Settings.
- Added Project Workflow using the existing project/rule-pack/scanner APIs, progress/cancel, report opening and File Inventory registration.
- Added English/Danish manual source/PDF resources and a local first-run tutorial.
- Complete suite: 48 passed. Packaged v0.4.1 TEST build completed; full Word acceptance remains pending.
