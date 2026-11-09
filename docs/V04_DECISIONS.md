# v0.4 beslutningslog

## D-001 — adapters frem for rewrite

Eksisterende moduler og dataformater bevares bag adapters; v0.4 AppShell må ikke kræve en simultan omskrivning.

## D-002 — independent language dimensions

UI, source og target language lagres separat; ingen norsk/dansk antagelse i core.

## D-003 — canonical schema with explicit migrations

Legacy CSV importeres via navngivne adapters og aldrig ved tavs kolonnefortolkning.

## D-004 — local-first privacy

Ingen telemetry eller external document upload; prompts er lokale tekstressourcer uden AI API.
