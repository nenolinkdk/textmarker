# Nenolink Text Tools v0.4.1 — implementation plan

Phase A (this commit): establish specification, architecture, acceptance cases, privacy/compatibility risks and decision records.

Phase B: complete packaged acceptance before new usability work. Run the full suite and packaged startup/resource smoke test; exercise project-to-report scanning, rule-pack and Prompt Library workflows, Danish/Norwegian Word Index and repeated/cancelled runs. Prepare synthetic Word fixtures with split runs, existing formatting and tables. Record manual Word checks separately.

Phase C: implement only after Phase B approval. Add persistent UI locale preference, expanded contextual guidance, Help/manual access and the tutorial shell. Add localization, lifecycle, backward-compatibility and packaged GUI tests. Keep scanner windows and File Inventory storage unchanged.

Phase D (future): implement the FSM Prompt Builder and concept-oriented Terminology module only after a separate approved specification. Format interoperability work remains a separate decision.

Phase gates:

- Every phase has a separate commit and documentation update.
- No phase may claim packaged or Microsoft Word acceptance without executing it.
- No source or generated output may overwrite an input or an existing published result.
- Stop after Phase A and wait for approval before implementation.
