# v0.4 testplan

Preserve the complete v0.3 suite. Add tests for six UI locales, key completeness/fallback, language independence, project persistence and directory validation, legacy/canonical rule adapters, rule pack activation, GUI navigation, cancellation/repeated runs, inventory and no-overwrite.

Separate localization tests from linguistic rule coverage. Packaged Windows E2E must exercise representative workflows and verify bundled resources. DOCX XML tests are not a substitute for opening output in Microsoft Word without repair warnings.

Phase B automation covers six-language registry/validation, locale completeness/fallback, independent source/target pair, JSON project round-trip/invalid language and v0.3 adapter semantics. GUI redesign, Prompt Library and packaged build were intentionally not run.

Phase C automation covers navigation labels, five module routes, future-section labeling, locale switching, source/target independence, project profile save, contextual panel toggle, window lifecycle and existing v0.2/v0.3 regression behavior. Windows scaling and visual accessibility remain manual acceptance checks.

Phase D automation covers rule-pack import, v0.3 compatibility, duplicate protection, prompt loading/saving and functional workspace routes. Full individual rule editing/filter matrix and Windows visual scaling remain acceptance follow-up.

Phase E automation covers exact schema detection, CRUD persistence, active-pack references, missing/incompatible pack validation and scanner-adapter preconditions. Complete suite: 43 passed.
