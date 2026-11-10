# v0.5 Phase F acceptance matrix

## Automated

- Baseline before Phase F: 67 passed.
- Final Phase F regression suite: **68 passed, 0 failed**.
- Rule example schema: PASS (`data/examples/da_interference_rules.csv`).
- Six-locale module metadata and two-prose-paragraph structure: PASS.
- Offline help anchor/resource checks: PASS.

## Packaged

- Clean Windows TEST build: PASS.
- Process startup/responsiveness: PASS.
- Full packaged Terminology round trip: NOT TESTED in the available desktop session.
- Full packaged Prompt Builder wizard: NOT TESTED in the available desktop session.
- All 12 manual/help link click-throughs: NOT TESTED in the available desktop session.

## Manual Word

- Word repair-warning and visual formatting inspection: NOT TESTED in this Phase F run. Existing user-reported Word acceptance is retained as user-reported evidence only.

## Linguistic documentation

- Danish/English content: implemented and reviewed for functionality scope.
- Swedish, Norwegian Bokmål, German and French: resources exist and are structurally tested; professional linguistic review remains outstanding.

## Limitations

Mapping profiles now have GUI controls and header compatibility checks. Generated concept IDs are explicit and never infer concept equivalence. Duplicate preview remains repository-level candidate detection rather than automatic merge.
