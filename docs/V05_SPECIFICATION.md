# Nenolink Text Tools v0.5 — Phase A specification

Status: documentation-only architecture baseline. No v0.5 application code is implemented.

## Baseline and acceptance record

- Branch base: v0.4.1 commit `8bfdf0c8cdeb377eb4f4a1ca85c8b851301a1295`.
- Reference EXE: `dist-text-tools-0.4.1/Nenolink-Text-Tools-0.4.1-TEST.exe`.
- Reference EXE size: 51,862,073 bytes.
- Reference EXE SHA-256: `FAE5E6B06ACC38291D20150EB96BA2C0160ACC7F35F8C9F04CE888136E7F1D40`.
- v0.4.1 automated result: 48 passed; the packaged process started successfully.
- The user reports that Microsoft Word opening and visual inspection were completed. This is recorded as user-reported acceptance, not independently reproduced by Codex.
- Broader packaged workflow and acceptance testing remain planned; comprehensive acceptance is not claimed.

## Product direction

v0.5 evolves the local application into multilingual translation QA and terminology management while preserving Text Marker, Translation Risk Scanner, DA-interference scanner, Word Index, File Inventory, rule-pack and Prompt Library behavior.

## Constraints

All processing remains local and deterministic. No cloud AI, telemetry, licensing, payment, TMX, XLIFF or direct Trados integration is included in the v0.5 implementation scope. TBX is optional later work and cannot be described as supported until fixture and Trados interoperability tests pass.
