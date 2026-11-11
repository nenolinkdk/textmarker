# Nenolink Text Tools v0.5 – brukerhåndbok

Dette er en lokal håndbok for profesjonell oversettelsesrevisjon. Velg grensesnittspråk i Innstillinger; kilde- og målspråk er uavhengige valg og endrer ikke manuskriptet.

## Prosjekt og filformater

Opprett et prosjekt, velg arbeidsmappe og angi språkpar. Text Marker tar DOCX/TXT og ordlister i CSV, MD eller TXT og lager en ny markert DOCX. Translation Risk Scanner krever nøyaktig `expression,category,color,severity,explanation,suggestion,enabled`. Interference Scanner krever `rule_id,expression,language,category,severity,color,explanation,suggestion,enabled`. Canonical rule packs har elleve kolonner og skal ikke blandes med de eldre formatene.

Velg alltid en ny outputfil. Et funn er et kontrollsignal, ikke en bekreftet oversettelsesfeil; les kilde og måltekst i sammenheng før du endrer noe.

## Moduler og arbeidsresultat

Dashboard velger prosjekt og arbeidssteg. Project Workflow samler prosjekt, språk, rule packs og DOCX og lager sporbare rapporter. Text Marker søker etter bokstavelige uttrykk og markerer et separat DOCX. Translation Risk Scanner viser mulige falske venner og misvisende nordiske likheter fra syv-kolonne CSV. Language Interference Scanner bruker ni-kolonne regler og RED/ORANGE/YELLOW-markering; felles dansk/norsk/svensk ord kan være riktig. Word Index teller ord med valgfri dansk eller norsk stoppordliste og eksporterer CSV/TXT for terminologi- og interferensrevisjon.

File Inventory lagrer filstier og kan åpne eller gjenbruke filer, men er ingen sikkerhetskopi. Terminology lagrer konsepter, flere språk og termstatus i SQLite; kundedata mappes eksplisitt og dubbletter slås ikke automatisk sammen. Glossaries & Rules validerer og administrerer lokale rule packs. Prompt Library og Prompt Builder lager redigerbare lokale instruksjoner; ingen tekst sendes til en ekstern tjeneste. Settings lagrer UI-språk, språkpar og mapper. Help åpner de tilsvarende offline-prosedyrene.

## Praktiske tutorials

1. Norsk–dansk litterær revisjon: åpne Risk Scanner, velg norsk DOCX og `data/examples/risk_rules_no_da.csv`, angi output og start. Sammenlign markerte uttrykk med dansk måltekst; korriger bare når kontekst og regelbeløp støtter det.
2. Interferens: velg en ni-kolonne regelpakke, filtrer kategori, kjør og les occurrence-rapportens forklaring. Kandidat betyr ikke bekreftet feil.
3. Word Index: velg DOCX, velg `nb`, slå stoppord av/på og eksporter. Bruk høye frekvenser til termkontroll og let etter kildeformer.
4. Terminologi: opprett konsept, legg til dansk og norsk term, velg status, importer kundens CSV med kolonnemapping, vurder dubbletter og eksporter canonical CSV.
5. Text Marker: velg DOCX og en CSV/MD/TXT-liste, start og åpne den nye filen; originalen beholdes.
6. Regel-fil: kopier eksempelet, behold headeren, lagre UTF-8 og rett validation-feil før scanning.
7. Prompt Library/Builder: velg Terminologikonsistens, `nb`→`da`, skriv domene, rediger kriterier, se preview, lagre kopi og eksporter TXT. Det kjøres ingen AI-analyse.

## Feilsøking

Blandede eller ugyldige CSV-skjema avvises. Manglende input, eksisterende output og kansellering skal ikke gi ufullstendige publiserte filer. Åpne DOCX i Word for siste kontroll av reparasjonsvarsel og formatering. All behandling foregår lokalt.
