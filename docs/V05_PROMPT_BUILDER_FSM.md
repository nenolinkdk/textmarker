# v0.5 Prompt Builder FSM

The builder is local, deterministic and editable. It never calls a cloud service.

| State | Events | Guard | Next |
|---|---|---|---|
| SELECT_TASK | task_selected, reset | task is supported | SELECT_LANGUAGES |
| SELECT_LANGUAGES | languages_selected, back | valid independent UI/source/target pair | SELECT_DOMAIN / SELECT_TASK |
| SELECT_DOMAIN | domain_selected, back | non-empty domain | SELECT_CRITERIA / SELECT_LANGUAGES |
| SELECT_CRITERIA | criteria_saved, back | criteria pass local validation | SELECT_OUTPUT / SELECT_DOMAIN |
| SELECT_OUTPUT | output_selected, back | local output format/path valid | PREVIEW / SELECT_CRITERIA |
| PREVIEW | edit, save, back, reset | preview has no unresolved required tokens | PREVIEW / SAVED / SELECT_OUTPUT / SELECT_TASK |
| SAVED | edit, reset | stored template exists | PREVIEW / SELECT_TASK |

Events `cancel` and `reset` are valid from every non-terminal state and clear transient state without altering the last saved template. Back navigation restores prior inputs. Invalid guards keep the state and expose field-level errors. Templates contain purpose, required input, editable text, expected output, limitations and validation instructions.
