# v0.2 test plan

- Regression: all existing TextMarker/Risk Scanner tests.
- Launcher: three routes, return-home, legacy entry-point isolation and worker cancellation.
- Word Index: DA/NB Unicode tokens, Danish ordering, punctuation/hyphen/apostrophe/numbers, exact stopwords, counts, BOM CSV/TXT, unsafe OOXML warnings, source/output safety and rollback.
- Inventory: register/search/sort/open/remove-reference, duplicate paths, missing files, persistence across restart, corruption/migration and no physical deletion.
- Windows: clean pinned environment, Qt import, actual visible launcher, end-to-end scan/index/inventory workflows, cancellation and no-overwrite behavior. Word repair-warning validation only if Word is available.
