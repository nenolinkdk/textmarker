# Nenolink Text Tools v0.5 – användarhandbok

Detta är en lokal arbetsbok för professionell översättningsgranskning. Välj gränssnittsspråk i Inställningar; käll- och målspråk är separata val och ändrar inte dokumentets text.

## Arbetsflöde och filer

Skapa eller välj ett projekt, ange arbetsmapp och välj språkpar. Text Marker använder DOCX/TXT och en ordlista i CSV, MD eller TXT och skapar ett nytt markerat DOCX. Translation Risk Scanner använder en risk-CSV med exakt `expression,category,color,severity,explanation,suggestion,enabled`; resultatet är markerad DOCX samt occurrence- och valfri summary-CSV. Language Interference Scanner använder nio kolumner: `rule_id,expression,language,category,severity,color,explanation,suggestion,enabled`. Canonical rule packs använder elva kolumner enligt regelpackens schema och får inte blandas med de två äldre formaten.

Öppna aldrig resultat över originalet. Välj en tom eller ny outputfil, kör kontrollen och öppna sedan resultatet från resultatraden. Markeringar är granskningskandidater, inte bevis på fel; läs alltid den omgivande käll- och måltexten.

## Moduler

| Modul | Indata och inställning | Resultat och språklig användning |
|---|---|---|
| Dashboard | Projekt, källspråk och målspråk | Öppnar rätt arbetsflöde utan att ändra manuskriptet. |
| Project Workflow | Projektmapp, kompatibla rule packs och DOCX | Spårbar markerad DOCX, rapporter och inventarier. |
| Text Marker | DOCX/TXT, CSV/MD/TXT-lista, skiftläges- och helordsval | Visar uttryck för terminologi- och redaktionskontroll. |
| Translation Risk Scanner | DOCX och sju-kolumners risk-CSV | Hittar möjliga falska vänner och vilseledande likheter; kontrollera kontext. |
| Language Interference Scanner | DOCX och nio-kolumners DA-regler | RED/ORANGE/YELLOW-kandidater för källspråklig interferens. Gemensamma nordiska ord kan vara korrekta. |
| Word Index | DOCX/TXT, danska eller norska och stoppordsval | Frekvenslista för terminologi, upprepning och möjliga interferensmönster. |
| File Inventory | Lokala filreferenser | Sök, öppna eller återanvänd befintliga filer; inventariet är ingen säkerhetskopia. |
| Terminology | SQLite-termbas eller kund-CSV med explicit kolumnmappning | Koncept, termer, språk, status och deterministisk canonical CSV. Möjliga dubbletter slås inte ihop automatiskt. |
| Glossaries & Rules | Validerad regel- eller glossary-CSV | Lokala rule packs med stabila ID:n och projektkoppling. |
| Prompt Library | Lokal mall, språk, domän, kriterier och outputstruktur | Redigerbar prompt; ingen text skickas till en AI-tjänst. |
| Settings | UI-språk, språkpar och arbetsmappar | Sparad lokal konfiguration. |
| Help | Modul-ID och offline-ankare | Procedurer, format, exempel och begränsningar. |

## Numrerade guider

1. Norsk–dansk litterär revision: öppna Risk Scanner, välj en norsk DOCX och `data/examples/risk_rules_no_da.csv`, välj output, kör scan och jämför varje markering med den danska översättningen. En falsk vän är en kandidat; ändra först efter mänsklig kontroll.
2. Interferens: välj en kompatibel nio-kolumners regel-CSV, filtrera kategori, kör och läs förklaring/suggestion i occurrence-rapporten. En kandidat är inte ett bekräftat fel.
3. Word Index: välj DOCX, språk `nb` eller `da`, slå stoppord på eller av, exportera CSV och granska höga frekvenser som terminologi- eller stilkandidater.
4. Terminologi: skapa koncept, lägg till termer på två språk, välj status, importera kund-CSV, mappa kolumner, visa dubblettkandidater, bekräfta och exportera; käll-CSV:n lämnas orörd.
5. Text Marker: välj separat DOCX och ordlista, aktivera helord vid behov, kör och öppna det nya DOCX:et. Originalet skrivs inte över.
6. Regel-CSV: kopiera ett bundlat exempel, behåll exakta headers, spara UTF-8, validera och korrigera fel kolumner eller severity innan scan.
7. Prompt Library/Builder: välj mall, ange Norsk bokmål → Dansk och litterär genre, lägg till kriterier, redigera preview, spara personlig kopia och exportera TXT. Prompten analyserar inte text själv.

## Begränsningar och felsökning

Felaktiga eller blandade CSV-scheman avvisas. Saknade filer, befintliga outputfiler och avbrutna körningar publicerar inte ofullständiga resultat. DOCX bör öppnas i Microsoft Word för manuell kontroll av reparationsvarningar och formatering. All behandling är lokal.
Text Marker-färger: TXT kan använda `uttryck%färg` och CSV använder kolumnen `color`. Utan färg används `yellow`. Använd `%%` för ett bokstavligt procenttecken.
