# v0.3 arkitektur

`Launcher -> DAInterferenceWindow -> DAInterferenceWorker -> da_interference.Scanner -> shared DOCX highlighter/reporter`

DA-scanneren holdes adskilt fra `textmarker.risk`. Den modtager immutable regler og valgte kategorier, returnerer deterministiske findings med stabilt rule-id og skriver først output efter komplet behandling. Workerens Qt-signaler følger samme progress/cancel-kontrakt som v0.2.

## Fremtidig Mode B

Scannerens inputgrænse er en analyse-session med dokumenter og paragraph-id’er, så en senere alignment-service kan tilføjes uden at blande state ind i GUI eller regelmotor. v0.3 konkluderer ikke betydningsskift.

## DOCX-sikkerhed

Originalen åbnes read-only. Markerede kopier bruger eksisterende run-aware OOXML-infrastruktur. `w:highlight` bruges til standardfarver; ORANGE kræver eksplicit `w:shd`-undersøgelse og skal testes i Word. Uunderstøttede strukturer rapporteres og behandles fail-safe.
