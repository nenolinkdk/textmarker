# v0.5 terminology module specification

## Entities

- `Concept`: stable concept ID, project/client association, domain/subject field, definition, notes and lifecycle timestamps.
- `TermEntry`: stable term ID, concept ID, language code, term text, grammatical/status metadata, approval status and source/reference.
- `ConceptSource`: source ID, URI or document reference, citation and import batch.
- `ProjectConcept`: project/client association and optional domain override.

One concept may contain many terms in one language and many languages. Missing language entries remain missing; they are never inferred as translations.

## Status and rule projection

Approval values are `proposed`, `approved`, `forbidden`, `deprecated` and `needs-review`. Approved terms may be exported to an explicitly named scanner rule pack. Forbidden terms may become review rules. The generated rule stores concept/term provenance and a projection version. Changing a termbase never mutates the original imported rule CSV.

## Operations

SQLite migrations are numbered and transactional. Search indexes normalized term text and language; filters cover project, client, language, subject, status and approval. Imports are staged by batch and can be rolled back. Duplicates are detected by normalized `(concept, language, term)` plus source provenance; possible duplicates require review. Backups are timestamped SQLite copies with integrity checks.

Phase B storage implements schema version 2. Migration v1→v2 adds concept notes after creating a sibling backup. A database with a newer `PRAGMA user_version` is rejected before writes. The repository uses foreign keys and transaction-scoped context managers; failed inserts/updates roll back. Term uniqueness is scoped to concept, language, normalized expression and status, so identical expressions may exist in distinct concepts.

Repository API: `create_concept`, `get_concept`, `update_concept`, `delete_concept`, `add_term`, `get_term`, `update_term`, `remove_term`, `terms_for_concept`, `search`, `add_source`, `associate`, `possible_duplicates`, `integrity_check` and `backup`. `TerminologyProjection` is intentionally read-only and raises `NotImplementedError` until an explicit future mapping is approved.

## Import/export

Import maps customer columns explicitly and records the mapping. Export is canonical UTF-8 CSV with stable IDs and deterministic ordering. Round-trip tests compare concepts, terms, statuses, provenance and associations, not only rendered text.
