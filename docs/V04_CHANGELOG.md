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

## Phase E

- Added exact v0.2/v0.3/v0.4 CSV schema detection; ambiguous headers are rejected.
- Added persistent rule enable/disable/remove operations and project active-pack validation.
- Added explicit DA scanner integration adapter with language-pair checks.
- Complete suite: 43 passed.
