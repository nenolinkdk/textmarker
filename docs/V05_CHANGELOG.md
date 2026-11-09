# v0.5 changelog

## Phase B

- Added `textmarker.terminology.repository`, a local concept-oriented SQLite repository.
- Added schema version 2 with transactional initial creation and v1→v2 migration.
- Added stable concept/term IDs, normalized language tags, multilingual terms, status validation, source/client/project associations, deterministic search and duplicate candidates.
- Added integrity checks, backup/recovery and unsupported newer-schema protection.
- Added 9 terminology repository tests; complete suite: **55 passed**.
- No GUI, import/export, TBX or scanner integration was added.
