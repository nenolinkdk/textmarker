# v0.5 changelog

## Phase B

- Added `textmarker.terminology.repository`, a local concept-oriented SQLite repository.
- Added schema version 2 with transactional initial creation and v1→v2 migration.
- Added stable concept/term IDs, normalized language tags, multilingual terms, status validation, source/client/project associations, deterministic search and duplicate candidates.
- Added integrity checks, backup/recovery and unsupported newer-schema protection.
- Added 9 terminology repository tests; complete suite: **55 passed**.
- No GUI, import/export, TBX or scanner integration was added.

## Phase C

- Added Terminology workspace to AppShell with CRUD/search/filter and destructive-operation confirmations.
- Added transaction-safe canonical terminology CSV preview/import/export with UTF-8/BOM, delimiter detection, duplicate validation and no-overwrite export.
- Added GUI/CSV regression tests; complete suite: **59 passed**.
- Interactive customer-column mapping profiles remain a follow-up limitation; TBX, scanner projection and Prompt Builder remain out of scope.

Packaged v0.5 TEST build completed with the Terminology module included. Microsoft Word, TBX and end-user customer-spreadsheet acceptance remain outside this phase.

## Phase C2

- Added compact localized module introductions covering purpose, input, output, use and workflow.
- Added stable offline help anchors and packaged help resource validation tests.
- Added guided source-column mapping dialog and reusable profile storage with header compatibility checks.
- Added central application version `0.5.0`.
- Complete suite: 61 passed.

## Phase D

- Added deterministic Qt-independent Prompt Builder FSM and local editable prompt persistence.
- Added six review-safe initial templates covering terminology, interference, risk, style, completeness and technical documentation.
- Added Prompt Builder GUI with editable preview, clipboard copy and local save/reopen.
- Complete suite: 65 passed.

The v0.5 TEST executable was rebuilt from the Phase D sources; packaged Prompt Builder click-through is still a manual acceptance item.

## Phase E

- Expanded all 12 module introduction pages with localized prose and retained structured input/output guidance.
- Documented Prompt Builder and added its offline help anchor.
- Added explicit generated-concept-ID choice to customer CSV import.
- Complete suite: 67 passed.

## Phase F

- Completed mapping profile controls and explicit generated-concept-ID option.
- Added bundled DA-interference rule example and documented actual CSV schema.
- Added linguistic-purpose/help documentation and Phase F acceptance matrix.
- Final suite: 68 passed.

## Phase G

- Audited the implemented CSV parsers and corrected offline help so Translation Risk, DA-interference and canonical rule-pack schemas are not conflated.
- Added explicit help anchors for DA-interference rules and the first-run tutorial.
- Added release-candidate acceptance evidence and separated automated, packaged and manual Word verification statuses.
- Rewrote Danish and English module introductions with concrete source material, settings, processing, outputs and linguistic review use; added a twelve-module documentation coverage matrix.
- Rebuilt the Windows TEST executable after the introduction-text update; packaged startup remained responsive.
