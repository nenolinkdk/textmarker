# v0.3 beslutningslog

## D-001 — separat regelmotor

DA-interferensregler må ikke genbruge Translation Risk Scanner-state; det reducerer regressionsrisiko og gør fremtidig bilingual alignment mulig.

## D-002 — review-indikatorer

RED/ORANGE/YELLOW er kategorier for menneskelig kontrol, ikke påstande om fejl.

## D-003 — sikker publicering

Originalen må aldrig være outputmål. Alle outputfiler reserveres uden overwrite og ryddes ved fejl/cancellation.

## D-004 — orange OOXML

`w:shd` undersøges for orange, fordi standard `w:highlight` ikke har orange. Word-kompatibilitet dokumenteres ud fra testresultater.
