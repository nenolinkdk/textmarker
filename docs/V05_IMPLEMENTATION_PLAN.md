# v0.5 implementation plan

## Phase B — terminology data model and storage

Deliverables: SQLite schema, migrations, repository, backup/restore and deterministic search. Tests: migration, rollback, Unicode, duplicate handling, invalid state and backward compatibility. Risk: project data corruption; acceptance requires atomic writes and integrity checks.

## Phase C — terminology GUI and CSV

Deliverables: concept/term editor, search/filter, explicit customer-column mapping, import error report and safe canonical export. Tests: CRUD, multilingual entries, round trip, duplicate review and no-overwrite.

## Phase D — FSM Prompt Builder

Deliverables: state machine, editable local templates, validation, back/reset/cancel and persistence. Tests: transition table, guards, invalid input, restart and no-network behavior.

## Phase E — contextual HTML help and tutorials

Deliverables: versioned help catalog, stable IDs/anchors, offline HTML/PDF generation, control mapping, localized procedures and tutorial. Tests: broken IDs/anchors/resources, packaged links and locale fallback.

## Phase F — optional TBX interoperability

Deliverables: only after approval, explicit TBX profile adapter and fixture matrix. Tests: round trip, unsupported fields, status/language mapping and tested Trados/MultiTerm observations.

## Phase G — packaged acceptance and stabilization

Deliverables: clean Windows TEST build, packaged E2E, failure/cancellation/restart tests, Word manual acceptance and release-blocker report. No release without explicit approval.

Every phase has a separate commit, documentation update, regression run and stop gate.
