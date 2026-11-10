# v0.5 implementation plan

## Phase B — terminology data model and storage

Deliverables: SQLite schema, migrations, repository, backup/restore and deterministic search. Completed in Phase B with schema version 2. Tests: migration, rollback, Unicode, duplicate handling, invalid state and backward compatibility; complete suite 55 passed. Risk: project data corruption; acceptance is protected by atomic writes, foreign keys and integrity checks.

## Phase C — terminology GUI and CSV

Deliverables: concept/term editor, search/filter, CSV preview/validation and safe canonical export. Phase C completed the GUI and canonical import/export; arbitrary customer-column mapping profiles and full import error dialog remain before this phase can be considered complete. Tests: CRUD, multilingual entries, round trip, duplicate review and no-overwrite.

## Phase D — FSM Prompt Builder

Deliverables: state machine, editable local templates, validation, back/reset/cancel and persistence. Completed in Phase D with explicit guards and 65 passing tests. Packaged wizard click-through remains an acceptance step.

## Phase E — contextual HTML help and tutorials

Deliverables: versioned help catalog, stable IDs/anchors, offline HTML/PDF generation, control mapping, localized procedures and tutorial. Tests: broken IDs/anchors/resources, packaged links and locale fallback.

## Phase F — optional TBX interoperability

Deliverables: only after approval, explicit TBX profile adapter and fixture matrix. Tests: round trip, unsupported fields, status/language mapping and tested Trados/MultiTerm observations.

## Phase G — packaged acceptance and stabilization

Deliverables: clean Windows TEST build, packaged E2E, failure/cancellation/restart tests, Word manual acceptance and release-blocker report. No release without explicit approval.

Every phase has a separate commit, documentation update, regression run and stop gate.
