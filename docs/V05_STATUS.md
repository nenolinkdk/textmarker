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
