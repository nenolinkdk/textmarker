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

## Import/export

Import maps customer columns explicitly and records the mapping. Export is canonical UTF-8 CSV with stable IDs and deterministic ordering. Round-trip tests compare concepts, terms, statuses, provenance and associations, not only rendered text.
