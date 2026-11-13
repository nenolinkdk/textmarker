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

## Phase I.6.2e verification

| Requirement | Implementation | Automated test | Packaged GUI | Word |
|---|---|---|---|---|
| Six-locale AppShell navigation and context controls | IMPLEMENTED | PASS (83 tests) | PASS for startup/dashboard smoke; full language click-through NOT TESTED | NOT TESTED |
| Isolated Danish/Norsk language-switch regression | IMPLEMENTED | PASS | NOT TESTED end-to-end | NOT TESTED |
| Fresh Windows TEST build | IMPLEMENTED | PASS | PASS: process remained alive for 5 seconds | NOT TESTED |
| Secondary-window full localization audit | PARTIAL | Catalog/window tests PASS; legacy strings remain to audit | NOT TESTED | NOT TESTED |
| Manuals/tutorial semantic and native-language review | PARTIAL | Resource/anchor tests PASS | NOT TESTED from packaged browser | NOT TESTED |

Build commit: fe2ac6ca3c6cf14ebd461b9a90a3da8b74bc1ab7  
EXE: dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe  
Size: 51,987,920 bytes  
SHA-256: E0D3A01DA51807AFCF664F3AA5181A538D1B84A1C875AEC1BA2B8BA1F6AF577

## Phase I.6.3 GUI acceptance

| Requirement | Automated | Packaged GUI | Status / evidence |
|---|---|---|---|
| Compact introduction layout without large vertical spacers | PASS, 90 tests | PASS | Shared `ModuleIntroduction` uses compact margins, cards and no stretch spacer in the central workspace. |
| Pastel information cards with dark-theme contrast | PASS | PASS | Introduction, workflow and result cards use shared Qt styling; dark-theme screenshot visually checked. |
| Numbered guidance on every module introduction | PASS for all six locales | PASS for Dashboard and Translation Risk Scanner | Four concrete numbered steps are visible and localized; full twelve-module manual click-through remains NOT TESTED. |
| Module-specific right help panel | PASS | PASS | Panel includes selected module title, purpose, input and output; full workflow-specific wording for all locales remains NOT TESTED. |
| Preserve module fields across navigation | PASS | NOT TESTED across all modules | Open module instances are cached and reused; regression test verifies Risk Scanner file selection survives navigation. |
| Preserve state across UI-language switching | PASS for AppShell/introduction state | NOT TESTED manually in packaged EXE | Existing language-switch tests plus new state tests pass. |
| Six-language manuals/tutorials | Resource tests pass | NOT TESTED | Existing localized resources are bundled; full linguistic/manual workflow review remains pending. |
| Fresh Windows TEST.exe | PASS | PASS | Separate process remained alive for 5 seconds. |
| Microsoft Word DOCX acceptance | Existing DOCX tests pass | NOT TESTED | Requires manual opening in Microsoft Word. |

Phase I.6.3 code/build commit: `324598ea6ec60e25138bf53584a08ea4f9bc9470`  
Automated tests: **90 passed, 0 failed**  
EXE: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`  
Size: `51,995,817` bytes  
SHA-256: `7B5DB2A00F6EA4CEF0349E5D9B3896841DF9B2C58007C50C5A46D5D993E09043`

## Phase I.6.3b — acceptance note

The former four-item HTML list was replaced by `StepGuide`, a modeless scrollable Qt guide. Text Marker exposes six concrete steps and Project Workflow exposes six concrete steps naming the visible controls. The current step is retained by the module introduction while navigating and changing locale. Project Workflow is placed inside a scroll area. Bundled Text Marker examples are present in `data/examples/`.

Automated: 93 passed, 0 failed. Windows build from commit `3a7daee9c0575d2d6174624c60efde7404338227`: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 52,038,454 bytes, SHA-256 `A0902080817556A8C938A9CE97E38EC8FF9731C4269C5AB7D0476613DD374E8B`. Packaged process launch was observed. Visual packaged Previous/Next, scrollbar and screenshot acceptance were not completed because the CUA window index did not expose the launched window; Microsoft Word acceptance remains manual/not tested.
## Phase I.6.3c

The guide now exposes localized example actions for Text Marker and replaces its generic fallback troubleshooting with concrete file/status guidance. Automated regression suite: 94 passed. Build commit `c6b0cc1ee6a8f75b76fbb43f85a049e76365d0af`; EXE size 52,040,229 bytes; SHA-256 `51E06AD5018492A6BB04A25F16EC5FB4B769965F7B0AC6111725223206470227`. Packaged visual navigation and screenshots were not testable through the available CUA window index; Word validation remains manual/not tested.
