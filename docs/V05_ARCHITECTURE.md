# v0.5 architecture

`AppShell -> Navigation -> Workspace + ContextPanel` remains stable. Shared services are local and Qt-independent:

`HelpCatalog -> UI/manual/tutorial adapters`

`ProjectProfile -> TerminologyStore + RulePackStore -> Scanner adapters`

The terminology store is separate from scanner rules. Approved or forbidden term entries can be projected into an explicit scanner-rule export, but the original termbase record and provenance remain unchanged. No scanner silently consumes termbase data.

## Storage

Use a versioned SQLite database per user/project with migrations. Concepts, terms, definitions, sources, statuses and project associations are normalized. SQLite transactions, atomic backup and schema version checks protect user data. Invalid optional state must not prevent application startup.

## Living documentation

Versioned Markdown/JSON content is the single source for contextual help, procedures, anchors, local HTML, generated PDF and tutorial steps. Each UI control declares a stable help ID. A build-time validator rejects duplicate IDs, missing anchors, unresolved cross-links and missing bundled resources.

## Compatibility boundary

Existing rule packs and scanner APIs remain adapters. Termbase-to-rule projection is one-way and explicit. TBX is isolated behind a later adapter so unsupported fields cannot be dropped silently.
