# Nenolink Text Tools v0.4.1 — Phase A architecture

## Shell and preference boundary

`AppShell -> Navigation -> Workspace + ContextPanel` remains the v0.4 structure. A `UiPreferences` service owns only UI locale and tutorial state. `ProjectProfile` continues to own source language, target language and working directories. These stores must not share mutable language state.

The UI-language selector is persistent near Settings and emits a locale-change event. Safe runtime changes update shell-owned labels and context help. Legacy windows may require a restart; the UI must state this explicitly and never pretend a partial switch is complete.

## Help and manual content

Help is keyed by stable module identifiers and translation keys, not widget text. A `GuidanceCatalog` supplies short inline explanations and expanded contextual sections. A manual generator consumes the same keys plus screenshots/sample descriptions, so documentation and UI do not drift. PDF rendering is isolated from scanner cores.

## First-run tutorial

The tutorial is a finite sequence: `NotStarted -> Welcome -> ChooseModule -> RunSample -> ReviewOutput -> Complete`, with `Skipped` and `Cancelled` exits. Samples are bundled read-only fixtures; generated results use a temporary/user-selected tutorial output directory and are registered only when explicitly requested.

## Future Prompt Builder FSM

The planned builder uses states `Idle`, `SelectingTemplate`, `EditingInputs`, `Validating`, `Previewing`, `Saving`, `Saved`, `Cancelled` and `Failed`. Only validated local data may enter `Saving`; cancellation before publication removes temporary artifacts and leaves prior templates unchanged. No network/API state exists in this design.

## Future Terminology model

`TerminologyProject -> Concept -> TermEntry[]`. A concept has a stable ID, domain, definition and notes. Each term entry has language, term text, grammatical/status metadata and optional source. Source and target entries are independent; missing entries are represented as missing coverage, never inferred translations.

## Interoperability evaluation boundary

Later evaluation will use explicit adapters and fixture matrices for TBX, TMX and XLIFF. The matrix will record version, encoding, language metadata, inline markup, IDs, round-trip behavior and Trados observations. No parser or writer is introduced in v0.4.1 Phase A.
