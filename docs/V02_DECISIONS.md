# v0.2 decisions

- 2026-11-07: Base v0.2 on `feature/translation-risk-scanner-v0.1` at issue start; PR #2 and PR #4 remain unmerged.
- 2026-11-07: Use a shared launcher with isolated module controllers, not copied processing implementations.
- 2026-11-07: Use SQLite for reference-only inventory because it supports safe querying, migrations and persistence without storing manuscript contents.
- 2026-11-07: Curated stopword lists are heuristic editable resources; they are not claimed to be verified corpus top-100 lists.
- 2026-11-07: Future languages extend a language-resource/tokenizer registry; v0.2 ships Danish and Norwegian Bokmål only.
