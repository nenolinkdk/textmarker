# Nenolink Text Tools v0.4.1 — Brugervejledning

## Start og privatliv

Start Windows TEST-programmet eller Python-entrypointet. Behandlingen foregår lokalt; dokumenter og rapporter uploades ikke.

## Hovedworkflow

Åbn **Project Workflow**, opret et projekt, vælg kilde- og målsprog, vælg projektmappe, importér kompatible canonical rule-pack CSV-filer, markér packs og aktivér dem, vælg derefter et DOCX og start scanning. Resultater gemmes i projektets `outputs`-mappe og registreres i File Inventory.

Programmet afviser inkompatible sprogpar, manglende packs, konflikter mellem rule IDs og eksisterende outputfiler. Annullering publicerer ikke ufuldstændige outputs.

## Moduler

Text Marker markerer udtryk i et separat DOCX. Translation Risk Scanner og Language Interference Scanner laver regelbaserede fund. Word Index tæller ord med valgfri dansk/norsk stopordsfiltrering. File Inventory gemmer lokale filreferencer. Glossaries & Rules håndterer lokale rule packs. Prompt Library gemmer lokale skabeloner uden AI-tjeneste.

## Farver og rapporter

Rød, orange og gul angiver review-prioritet, ikke bekræftede oversættelsesfejl. Brug occurrence- og summary-CSV sammen med det markerede DOCX.

## Fejlfinding og begrænsninger

Brug unikke outputnavne, kontrollér at rule packs passer til projektets sprogpar, og vær opmærksom på warnings for ikke-understøttede DOCX-strukturer. TBX, TMX og XLIFF er ikke implementeret. Microsoft Word-verifikation er stadig manuel.
