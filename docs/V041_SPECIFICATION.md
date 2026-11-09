# Nenolink Text Tools v0.4.1 — Phase A specification

Status: Phase A only; specification and architecture baseline. No implementation is included in this phase.

## Scope

v0.4.1 is a usability, documentation and acceptance increment on top of the verified v0.4 implementation. It must preserve the five existing processing modules, their output semantics and all existing File Inventory data.

The product remains local and deterministic. Manuscripts are not uploaded, telemetry is not added, and source files are never modified in place.

## Acceptance goals

1. The main shell exposes a persistent UI-language selector adjacent to Settings. The selected UI locale is stored as a user preference and is independent from project source and target languages.
2. Every existing module has concise inline guidance and detailed contextual help in the right panel. Guidance must state input expectations, output behavior, cancellation behavior and relevant limitations.
3. An English/Danish PDF manual is designed first, with stable translation keys and a layout/content model ready for Swedish, Norwegian Bokmål, German and French. PDF generation is a later implementation step.
4. First-run onboarding is designed around bundled synthetic samples only. It must be skippable, restartable from Help and unable to touch user manuscripts.
5. A future FSM-based Prompt Builder is specified but not implemented. Its states, transitions, validation and cancellation semantics are defined below.
6. A future concept-oriented Terminology module is specified but not implemented. Terms have language-aware entries and project-scoped metadata.
7. TBX, TMX and XLIFF interoperability is evaluated for a later phase, including Trados compatibility risks, without implementing import/export in v0.4.1.

## Explicit non-goals

No TBX/TMX/XLIFF support, AI/API integration, licensing, payments, release packaging, merge or tag is part of Phase A. Phase B must complete acceptance verification before Phase C changes the UI.

## Compatibility and privacy

The compatibility baseline is commit `da198e2` on the v0.4 branch. Legacy windows remain adapters around existing cores. Locale resources stay bundled/local. Sample files contain no user data. All future persistence must be atomic, versioned and backward-compatible; malformed optional state must not prevent application startup.

## Risks

- A shell change can regress legacy Qt windows; mitigate with navigation/lifecycle tests and packaged GUI tests.
- Long localized strings can overflow at 1366×768 and 125% scaling; mitigate with layout tests plus Windows visual acceptance.
- PDF fonts and Unicode shaping may differ by platform; embed fonts and verify Danish/Norwegian characters in rendered output.
- Trados interoperability is format/version-dependent; claims must be limited to tested files and documented as compatibility findings, not guarantees.
- Tutorial samples can accidentally become real inputs; use read-only bundled fixtures and explicit output directories.
