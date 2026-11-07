# Nenolink Text Tools v0.2 — Windows accepttjekliste

## Før test

- [ ] Brug en ren Windows 11-maskine eller ren brugerprofil.
- [ ] Kontroller at `Nenolink-Text-Tools-0.2-TEST.exe` starter uden Qt DLL-fejl.
- [ ] Kontroller at launcher-vinduet viser Text Marker, Translation Risk Scanner og Word Index.
- [ ] Kontroller at eksisterende TextMarker- og Risk Scanner-entrypoints stadig starter.

## Word Index

- [ ] Indeksér en DOCX med dansk tekst og tegnene `æ`, `ø`, `å`.
- [ ] Gentag med norsk bokmål og kontroller korrekt `A–Z, Æ, Ø, Å`-sortering.
- [ ] Test stopord til/fra og CSV/TXT med/uden frekvenstal.
- [ ] Kontroller progress, cancellation og at ingen delvist output efterlades.
- [ ] Kontroller at eksisterende outputfil aldrig overskrives.

## File inventory

- [ ] Registrér en lokal fil og kontroller path, størrelse, mtime og SHA-256 i SQLite.
- [ ] Ændr filen, kør registrering igen og kontroller at metadata opdateres.
- [ ] Kontroller at inventaret ikke flytter, sletter eller ændrer kildefilen.

## DOCX-integritet i Microsoft Word

- [ ] Brug en kopi af en realistisk DOCX med styles, tabeller, header/footer og eksisterende highlights.
- [ ] Kør hver relevant funktion, og åbn outputtet i Microsoft Word.
- [ ] Kontroller at Word ikke viser “Word found unreadable content” eller reparationsdialog.
- [ ] Kontroller at tekst, styles, tabeller, headers/footers og eksisterende formatering er bevaret.
- [ ] Gem og luk dokumentet i Word, åbn det igen og kontroller at det stadig er intakt.

## Dokumentation af test

Registrér Windows-version, Python/PyInstaller-build-id, inputstørrelse, tid, peak memory, outputstier, eventuelle Word-advarsler og EXE SHA-256. Microsoft Word-testen kan ikke erstattes af en ZIP/XML-integritetstest.
