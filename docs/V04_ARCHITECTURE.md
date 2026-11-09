# v0.4 arkitektur

`AppShell -> Navigation -> Workspace + ContextPanel`

Workspace-moduler implementerer adapters for eksisterende funktioner: Text Marker, Translation Risk Scanner, Language Interference Scanner, Word Index, File Inventory, Glossaries & Rules, Prompt Library, Settings og Help. Core services er uafhængige af Qt:

`DocumentReader -> Extractor -> Matcher -> RuleEvaluator -> Finding -> Annotator/Reporter`

En canonical `Finding` indeholder rule pack, rule id, source/target language, expression, location, category, severity, explanation, suggestion og context. Legacy scanners beholder adapters og deres filformater. Project profiles ejer kun konfiguration; File Inventory ejer reference-metadata, aldrig dokumentindhold.

Risici: Qt-rewrite kan bryde legacy windows; løses med adaptere og regressionssuite. Orange OOXML og tracked changes kræver fortsat Word-verifikation. Manglende rule packs må vises som manglende coverage, ikke som fuld sprogunderstøttelse.

Phase E's `scan_project` validates active-pack availability and exact source/target pair before invoking the DA scanner.

Phase F merges explicitly associated compatible packs in sorted pack-ID order. Identical duplicate rules are deterministic; conflicting definitions are rejected.
