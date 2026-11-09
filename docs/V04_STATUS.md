# v0.4 status

- Branch: `feature/multilingual-text-tools-v0.4`
- Base commit: `b63aac6eda53ef4c6f3f74c7b11ea6ff41d02b1c`
- Phase A: gennemført i `2856aae63684736ce7355d256e5531e3b8ccf320`.
- Phase B: language registry, seks locale resources, fallback/missing-key API, project profiles, canonical models, legacy adapters og pipeline interfaces implementeret lokalt.
- Draft PR: afventer branch push/GitHub API.
- Tests: baseline **34 passed**; complete suite efter Phase B **38 passed**.
- Compatibility: eksisterende scanners og File Inventory er ikke ændret; adapters er additive.
- Phase B commit: `bc4e5daf3b24233db65890a5dc1c59edeca97cca`.
- Phase C: AppShell, navigation, central workspace, collapsible contextual panel, Settings, independent language selectors og project profile save implementeret.
- Tests: complete suite **39 passed**.
- Phase C commit: afventer commit efter dokumentationsopdatering.
- Phase D: lokale RulePackStore/Glossaries & Rules og PromptStore/Prompt Library implementeret; legacy imports er eksplicitte og filer overskrives ikke.
- Tests: complete suite **42 passed**.
- Phase D commit: afventer commit efter dokumentationsopdatering.
- Phase F: multi-pack scanner integration, conflict validation and project pack selection UI implemented.
- Tests: complete suite **44 passed**.
- Phase F commit: afventer commit efter documentation update.
- Phase E: explicit CSV schema detection, rule CRUD persistence, project pack associations and `scan_project` adapter implemented.
- Tests: complete suite **43 passed**.
- Phase E commit: afventer commit efter dokumentationsopdatering.
- Phase F build: `Nenolink-Text-Tools-0.4-TEST.exe`, Python 3.12 / PyInstaller 6.11.1, 51,839,819 bytes, SHA-256 `393867A873F78C4E2C668AE27E02C0BA362537C5818EB9B5B42496AE3E11A88C`.
- Manual Microsoft Word acceptance: not performed.
- Release blocker: packaged full workflow and Word repair-warning validation remain outstanding.
- Begrænsninger: translations, rule coverage, Word rendering og project migration skal implementeres og testes i senere faser.

## P0 hotfix: PyInstaller locale resources

- Root cause: the PyInstaller spec included `data` but not `src/textmarker/multilingual/locales`; package-data configuration alone did not add JSON resources to the executable.
- Fix: localization now resolves resources from source, frozen `_MEIPASS` bundle locations and `importlib.resources`, with a controlled missing-resource error. The clean build explicitly bundles all six locale JSON files.
- Also corrected AppShell navigation mapping so Settings opens the Settings page in the packaged shell.
- Verification: complete suite **46 passed**; packaged executable rebuilt and launched as a separate Windows process with a visible main window. Settings navigation was verified in the packaged GUI.
- Microsoft Word repair-warning validation remains manual and not performed.

## v0.4.1 Phase A

- Branch: `feature/text-tools-v0.4.1-usability`.
- Base: verified v0.4 hotfix commit `da198e2`.
- Phase A documentation is complete; no GUI, scanner, file-format or release changes were made.
- Phase B is intentionally pending approval.

## v0.4.1 Phase B

- Baseline suite: **46 passed, 0 failed**.
- Packaged startup/resource smoke: passed with the existing hotfix EXE.
- Complete packaged project workflow: blocked by missing AppShell controls for project/rule-pack association and project scanning.
- Module-specific packaged E2E and Microsoft Word manual acceptance remain pending.
