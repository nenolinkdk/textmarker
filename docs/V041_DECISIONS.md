# Nenolink Text Tools v0.4.1 — decisions

## D-041-001: Phase separation

Phase A is documentation-only. This keeps the usability contract reviewable before changing the stable v0.4 shell.

## D-041-002: Independent language ownership

UI locale belongs to user preferences; source/target languages belong to the selected project. A locale switch must never change scanner language-pair selection.

## D-041-003: Stable content keys

Guidance, tutorial and manual text use stable keys with English fallback and explicit missing-key detection. Raw translation keys are not acceptable end-user text.

## D-041-004: Local-only onboarding

The first-run tutorial uses bundled synthetic files and local outputs. It has no network path and no permission to access a real manuscript unless the user later selects one in an existing module.

## D-041-005: Interoperability claims

TBX, TMX, XLIFF and Trados compatibility will be reported as fixture-based observations only. No format support is implied by this design phase.

## D-041-006: Phase B scope control

The existing AppShell exposes module routes but not the complete project/rule-pack scanning workflow. Phase B records this as an integration blocker rather than adding unapproved Phase C usability functionality. No defect was fixed because no regression in the verified v0.4 baseline was reproduced.
