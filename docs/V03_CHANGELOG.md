# v0.3 changelog

## Phase A

- Oprettet krav, arkitektur, regel-schema, plan, testplan og beslutningslog for DA-interferensscan.

## Phase B

- Tilføjet independent DA-interference engine med strict CSV-validering, deterministic Unicode matching og stabile rule IDs.
- Tilføjet RED/YELLOW `w:highlight` og ORANGE `w:shd` med source-preserving DOCX output.
- Tilføjet occurrence- og summary-CSV med no-overwrite, cancellation og rollback.

## Phase C

- Tilføjet femte launcher-route `DA-interferensscan`.
- Tilføjet dansk GUI med DOCX/rule/outputvalg, kategorifilter, progress, cancellation og result-open.
- Registrerer input, regler og genererede outputs i eksisterende File Inventory.
- Tilføjet GUI-, lifecycle-, cancellation-, repeated-scan-, Unicode- og formatting-regressioner.

## Phase D

- Built `Nenolink-Text-Tools-0.3-TEST.exe` with bundled `data/` resources.
- Verified packaged launcher routes and actual packaged DA scan with RED/ORANGE/YELLOW output, occurrence report, summary report and inventory registration.
- Microsoft Word manual acceptance remains pending.
