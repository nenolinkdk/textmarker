# v0.2 test plan

- Regression: all existing TextMarker/Risk Scanner tests.
- Launcher: three routes, return-home, legacy entry-point isolation and worker cancellation.
- Word Index: DA/NB Unicode tokens, Danish ordering, punctuation/hyphen/apostrophe/numbers, exact stopwords, counts, BOM CSV/TXT, unsafe OOXML warnings, source/output safety and rollback.
- Inventory: register/search/sort/open/remove-reference, duplicate paths, missing files, persistence across restart, corruption/migration and no physical deletion.
- Windows: clean pinned environment, Qt import, actual visible launcher, end-to-end scan/index/inventory workflows, cancellation and no-overwrite behavior. Word repair-warning validation only if Word is available.
# Review regression additions

- Verify stopword resource resolution in source and frozen layouts.
- Verify GUI inventory option is present and enabled, and cancellation remains disabled until work starts.
- Verify inventory persistence and source immutability.
- Verify packaged launcher opens all three module routes; manual acceptance must execute each route end-to-end.
- Verify DOCX output in Microsoft Word without repair warnings; XML/ZIP checks alone are insufficient.
