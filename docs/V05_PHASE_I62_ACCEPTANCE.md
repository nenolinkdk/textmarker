# Phase I.6.2 acceptance status

## Implemented in this increment

- `ModuleIntroduction` now owns its widgets and refreshes their visible text without rebuilding or deleting the Qt layout.
- AppShell refreshes all currently instantiated module introductions after a UI-language change.
- Prompt Library built-in display names are localized for `da`, `sv`, `nb`, `en`, `de` and `fr`; stable task IDs and prompt bodies remain unchanged.
- Prompt Store persistence and UTF-8 export behavior remain unchanged.

## Verification

| Area | Status | Evidence |
|---|---|---|
| Existing regression suite | PASS | 77 passed, 0 failed |
| Runtime module-introduction refresh | PASS | launcher tests under `QT_QPA_PLATFORM=offscreen` |
| Stable language codes | PASS | existing source/target `currentData()` tests |
| Prompt template IDs and bodies | PASS | existing Prompt Store tests |
| Six complete localized module prose sets | PARTIAL | Danish and English are substantive; remaining locales need linguistic review and fuller module-specific copy |
| Six complete offline manuals | NOT COMPLETE | repository currently contains complete DA/EN source/manual artifacts only |
| Six practical tutorial sets | NOT COMPLETE | current bundled tutorial resources are shared/offline, not six fully localized tutorial sets |
| Packaged GUI click-through | NOT TESTED | requires Windows interactive verification |
| Microsoft Word visual acceptance | NOT TESTED | requires Microsoft Word |

The phase is not declared complete. No scanner algorithms, CSV schemas, terminology storage or FSM behavior were changed.

## Phase I.6.2b coverage matrix

`IMPLEMENTED` means a source resource exists; `AUTOMATED TEST PASSED` means the repository test checks its presence. `MANUALLY VERIFIED` is deliberately reserved for an interactive Windows check.

| Module | da | sv | nb | en | de | fr |
|---|---|---|---|---|---|---|
| Dashboard | IMPLEMENTED / AUTOMATED TEST PASSED | IMPLEMENTED / AUTOMATED TEST PASSED | IMPLEMENTED / AUTOMATED TEST PASSED | IMPLEMENTED / AUTOMATED TEST PASSED | IMPLEMENTED / AUTOMATED TEST PASSED | IMPLEMENTED / AUTOMATED TEST PASSED |
| Project Workflow | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Text Marker | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Translation Risk Scanner | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Language Interference Scanner | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Word Index | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| File Inventory | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Terminology | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Glossaries & Rules | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Prompt Library | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Settings | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |
| Help | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED |

The rows above document resource coverage, not linguistic approval. Full module-specific prose and secondary-window control localization remain `NOT TESTED`/`PARTIAL` pending native-language and packaged GUI review. No row is marked `MANUALLY VERIFIED`.

## Phase I.6.2c final verification matrix

| Requirement | Implementation status | Automated test | Manual verification | Remaining issue |
|---|---|---|---|---|
| Central secondary-window translation catalog | IMPLEMENTED for shared core controls | PASSED, 79 tests | NOT TESTED | Risk/DA/Terminology/Rules still contain legacy hardcoded field labels |
| Six-locale secondary-window instantiation | IMPLEMENTED/PARTIAL | PASSED for catalog coverage | NOT TESTED | Full visual text audit pending |
| Six manual source resources | IMPLEMENTED | PASSED for resource presence | NOT TESTED | Swedish/NB/DE/FR PDF output not generated |
| Six tutorial resource sets | IMPLEMENTED/PARTIAL | PASSED for added localized tutorial files | NOT TESTED | DA/EN shared tutorial still needs language-specific audit |
| Help anchors and bundled HTML | IMPLEMENTED | Existing anchor tests PASSED | NOT TESTED in packaged browser | Browser fragment behavior requires Windows check |
| Fresh packaged EXE | IMPLEMENTED | Build completed | Startup PASS; full click-through NOT TESTED | Interactive GUI acceptance remains |
| DOCX/Word acceptance | IMPLEMENTED by existing processing code | Existing regression tests PASSED | NOT TESTED | Microsoft Word unavailable in this session |

## Phase I.6.2d result

The shared catalog now covers the fixed application-owned strings used by the four named windows, and parameterized tests instantiate those windows under all six locales. This is an automated UI-control check, not a substitute for native linguistic review or interactive Windows acceptance.

Fresh build: source commit `5f2fcbd7032b25fe64cc5d3cd843d81c984b31a3`, EXE size `51,981,902` bytes, SHA-256 `39A7A9D315DD8550C93CD3A8273F4FF2D47A3219301B51246F8F0CE579533E96`. Separate-process startup: `PASS`. Full GUI click-through and Microsoft Word: `NOT TESTED`.
