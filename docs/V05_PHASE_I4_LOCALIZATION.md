# Phase I.4 localization and documentation coverage

`PASS` means verified in source or automated tests. `NOT TESTED` means packaged/manual verification is still required; it is not counted as complete localization.

| Area | da | sv | nb | en | de | fr |
|---|---|---|---|---|---|---|
| Locale resource loads | PASS | PASS | PASS | PASS | PASS | PASS |
| Translation-key completeness | PASS | PASS | PASS | PASS | PASS | PASS |
| AppShell runtime labels | PARTIAL | NOT TESTED | NOT TESTED | PARTIAL | NOT TESTED | NOT TESTED |
| Module-window labels | PARTIAL | NOT TESTED | NOT TESTED | PARTIAL | NOT TESTED | NOT TESTED |
| Module-specific prose | PASS | NOT TESTED | NOT TESTED | PASS | NOT TESTED | NOT TESTED |
| Offline manual chapters | PARTIAL | NOT TESTED | NOT TESTED | PARTIAL | NOT TESTED | NOT TESTED |
| Tutorials | PARTIAL | NOT TESTED | NOT TESTED | PARTIAL | NOT TESTED | NOT TESTED |

The application currently has six locale resource files and fallback validation, but several legacy secondary windows still contain hardcoded labels. This report therefore does not claim 100% localization. The v0.5 manual and tutorials are local Danish resources with documented English terminology where the implemented UI still uses product names; full six-language manual generation remains outstanding.

## Prompt Library acceptance

The first-launch library now displays six read-only built-in templates from `PromptStore.initial_templates()`. Personal prompts are stored in the user profile file and are never written back to bundled templates. Selecting a built-in and pressing Duplikér creates a personal copy; Gem tilpasset prompt, Åbn, and Eksportér tekst operate on personal data.
