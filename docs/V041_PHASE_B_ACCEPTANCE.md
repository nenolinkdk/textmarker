# v0.4.1 Phase B acceptance report

## Environment

- Branch: `feature/text-tools-v0.4.1-usability`
- Base/Phase A: `da198e2` / `ceffd826b898926f7b20d62a92de030397267e27`
- Python: 3.12.14
- PySide6: 6.7.3
- PyInstaller: 6.11.1
- Windows packaged artifact: `dist-text-tools-0.4-hotfix/Nenolink-Text-Tools-0.4-TEST-hotfix.exe`
- EXE size: 51,841,956 bytes
- EXE SHA-256: `26A068EDA43A7E4D68302537E4E416C8174CC2B57B34D8B32CB84CADEFAE7389`

## Automated verification

The complete local regression suite passed: **46 passed, 0 failed**. A pytest cache permission warning was emitted by the pre-existing workspace cache directory; it did not affect test execution.

Covered areas include localization resources, project persistence, rule-pack schema and CRUD behavior, scanner integration, DOCX highlighting/integrity, cancellation/rollback, Word Index, File Inventory and Qt lifecycle/navigation tests.

## Packaged verification

Passed:

- Onefile EXE launched as a separate Windows process.
- Main window `Nenolink Text Tools v0.4` became visible without a Python traceback.
- Navigation displayed all existing modules and future sections.
- Resource-loading hotfix remained functional in the packaged executable.

Not available as a complete GUI workflow:

- The current AppShell does not expose project creation, working-directory configuration, CSV rule-pack import/association or project-to-report scanning as shell controls. It opens existing compatible module windows instead. The corresponding core APIs are covered by automated tests, but the requested packaged GUI workflow is therefore blocked until a later approved usability/integration phase.
- Packaged GUI tests for the individual legacy windows and Word Index stopword toggles were not claimed as passed; they require module-specific fixture automation beyond the current shell routes.

## Failure handling

The automated suite covers missing inputs, malformed CSV, missing/conflicting packs, cancellation, repeated processing, rollback and no-overwrite behavior. No new defect was reproduced in this phase, so no application code or executable was changed.

## Microsoft Word acceptance

Pending. Representative acceptance cases are defined in `V041_IMPLEMENTATION_PLAN.md` and `V04_WINDOWS_ACCEPTANCE.md`: ordinary paragraphs, bold/italic and split runs, tables, existing highlights and tracked changes. Microsoft Word was not opened in this run, so repair-warning-free status and visual formatting preservation are not claimed.

## Phase C update

The AppShell now exposes Project Workflow, a persistent header UI-language selector synchronized with Settings, localized manual access and a five-step local tutorial. Project scanning uses the existing `scan_project` pipeline and registers source/output references in File Inventory.

## Release blockers

1. A full click-by-click packaged project-to-report run still requires fixture-driven GUI automation; the new packaged shell starts, but no Microsoft Word acceptance was performed.
2. Packaged module-specific E2E and Danish/Norwegian Word Index stopword checks remain outstanding.
3. Microsoft Word manual acceptance remains outstanding.
