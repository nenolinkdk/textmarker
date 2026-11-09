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
