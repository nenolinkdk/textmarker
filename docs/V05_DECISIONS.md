# v0.5 decisions

## D-0501 — Separate termbase and rules

Terminology is a concept-oriented source of truth. Scanner rules are derived artifacts with provenance, never an implicit second storage model.

## D-0502 — Explicit spreadsheet mapping

Customer bilingual spreadsheets are not assumed to be concept-oriented termbases. Import requires a visible mapping and validation preview.

## D-0503 — Local documentation source

Stable help IDs and versioned content drive UI guidance, offline HTML, PDF and tutorial. Missing content is a build error, not a runtime key leak.

## D-0504 — TBX claims are fixture-bound

TBX and Trados compatibility will be described only from executed fixture tests and named profiles/versions.

## D-0505 — Phase A boundary

This commit contains documentation only. No schema, GUI, scanner or file-format implementation is started before Phase B approval.
