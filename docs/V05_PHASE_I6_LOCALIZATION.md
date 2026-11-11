# v0.5 Phase I.6 localization and acceptance status

## Verified

| Area | Status | Evidence |
|---|---|---|
| Danish navigation labels | PASS | AppShell regression tests |
| Danish shell context text | PASS | Regression test rejects `Settings` and `Processing` boilerplate |
| User-facing language names | PASS | `language_name()` and selector tests |
| Internal language codes | PASS | Source/target selectors continue to use `currentData()` ISO codes |
| Six locale resources load | PASS | Existing localization test suite |
| Six structured Prompt Library templates | PASS | Template section, parameter and persistence tests |
| Clean packaged build | PASS | PyInstaller 6.11.1 / Python 3.12.14 |
| Packaged process startup | PASS | Separate process remained responsive for 8 seconds |

## Still requiring acceptance

| Area | Status | Notes |
|---|---|---|
| Complete localization of all secondary windows | PARTIAL | Legacy scanner and dialog strings still require a full six-locale audit |
| Six-language module prose and manuals | PARTIAL | Danish is the primary corrected locale; Swedish, Norwegian, German and French require linguistic review |
| Full packaged navigation and language-switch click-through | NOT TESTED | Source-level tests and startup smoke test are not a substitute for GUI acceptance |
| Offline manual/tutorial browser behavior in packaged EXE | NOT TESTED | Requires interactive Windows browser verification |
| Microsoft Word DOCX opening and visual formatting check | NOT TESTED | Requires Word on the target Windows installation |

The Phase I.6 build is therefore a test artifact, not a release claim.
