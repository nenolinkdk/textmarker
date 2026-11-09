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
