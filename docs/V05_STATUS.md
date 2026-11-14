# Nenolink Text Tools v0.5 status

## Phase B — terminology data model and persistence

- Branch: `feature/text-tools-v0.5`
- Phase A: `3b178ad5f2da485a48bfee94bfe14543d566450f`
- Phase B implementation: pending commit
- Schema version: **2**
- Automated suite: **55 passed, 0 failed**

Implemented: Qt-independent SQLite terminology repository, normalized BCP 47 tags, concept/term CRUD, multilingual terms, explicit statuses, sources, client/project associations, deterministic search/filtering, possible-duplicate detection, foreign keys, transactions, integrity checks, v1→v2 migration with backup, unsupported-newer-schema rejection and backup API.

Not implemented by design: GUI, CSV import/export, TBX, TMX, XLIFF, Prompt Builder, scanner projection and AI integration.

Known limitation: migration backups are retained beside the database and are not automatically rotated. Scanner integration has only a read-only `TerminologyProjection` boundary; no terminology record can affect existing scans.

## Phase C — terminology GUI and CSV

- Terminology workspace added to AppShell and uses the Phase B SQLite repository as its sole storage.
- GUI supports concept browsing/search, multilingual terms, status editing, definitions, subject fields, deletion confirmation and CSV import/export.
- CSV supports UTF-8/BOM, comma/semicolon delimiters, quoted fields, deterministic canonical export, filter export and overwrite protection.
- Automated suite: **59 passed, 0 failed**.
- Remaining limitation: the GUI import action currently auto-maps canonical headers; a full interactive customer-column mapping/profile dialog and row-by-row preview is still outstanding.

## Phase C completion

- Terminology route is available from AppShell and backed by `TerminologyRepository`.
- Canonical CSV preview/import/export is implemented with validation, transaction rollback and no-overwrite export.
- Complete suite: **59 passed, 0 failed**.
- Windows TEST EXE built successfully; the packaged process was started and remained responsive. GUI route verification is automated; direct packaged click-through of the Terminology page remains limited by the current desktop automation session.

## Phase C2 — module introductions and guided mapping

- Added reusable `ModuleIntroduction` metadata component for all 12 navigation items.
- Added stable help IDs and offline `docs/manual/help.html` anchors, bundled by PyInstaller.
- Added centralized `0.5.0` version definition used by the application title.
- Added interactive CSV mapping dialog with language selection and validation, plus local mapping-profile persistence API.
- Complete suite: **61 passed, 0 failed**.
- Packaged build completed; process started responsive. Direct packaged click-through of the mapping dialog remains pending in this desktop session.

## Phase D — Prompt Builder

- Added Qt-independent deterministic FSM with explicit states, guards, Back, Reset, Edit and Save transitions.
- Added local PromptStore CRUD, search, duplicate and text export, with six initial review templates.
- Added Prompt Builder window in the Prompt Library route with task/language/domain/criteria/output steps, editable preview, clipboard copy and local save/reopen.
- Complete suite: **65 passed, 0 failed**.
- Final packaged build completed; the executable process started and remained responsive. Full wizard click-through remains pending in the current desktop session.

## Phase E — complete user experience

- Added two connected prose paragraphs for each of the 12 module introductions in all six locale resources, while retaining structured INPUT/OUTPUT/USE/WORKFLOW sections.
- Added Prompt Builder help anchor and documentation for templates, editing, saving, reopening, copying, confidentiality and limitations.
- Added generated concept-ID option to guided CSV import; explicit mapping remains required for term and language, and concepts are never silently merged.
- Added regression coverage: **67 passed, 0 failed**.
- Final packaged GUI click-through remains limited by the desktop session; startup is verified after the final build.

## Phase F — final GUI completion and Windows acceptance

- Added GUI mapping-profile save, select, compatibility validation and delete controls.
- Added explicit generated concept-ID import option and bundled DA-interference CSV example using the actual supported schema.
- Added linguistic-purpose prose and scanner/rule documentation anchors.
- Final automated suite: **68 passed, 0 failed**.
- Acceptance matrix: `V05_PHASE_F_ACCEPTANCE.md`.

## Phase G — release candidate acceptance

- Baseline verified on `feature/text-tools-v0.5`, local HEAD `cb311617928e83e7644ec392d2aa7b6e2dfec169` before Phase G changes.
- Complete automated suite: **68 passed, 0 failed** (one PytestCacheWarning due to cache permissions).
- Actual parser audit completed for Translation Risk, DA-interference and canonical v0.4 rule packs. Documentation now distinguishes their schemas and includes `interference.rules` and `tutorial.overview` anchors.
- Push was attempted and blocked by network connectivity; the exact error is recorded in the Phase G acceptance report. Remote synchronization is not claimed.
- Packaged startup can be verified, but full packaged GUI click-through and Microsoft Word visual acceptance remain pending in this desktop session.
- New RC artifact: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 51,943,095 bytes, SHA-256 `DE5B5B1DFB3904B0D8F8A0A0FACCC6B9DD61FDA7E08A2BAE5487F1B5DF98F22C`; built from `830f4118e90d89e7ea0a84a16d4d316d63e26403`; separate-process startup remained responsive.
- Added the documentation coverage matrix in `V05_DOCUMENTATION_COVERAGE.md`. Danish and English now have module-specific linguistic input→processing→output prose; the four other locales remain flagged for native linguistic review.
- Rebuilt the v0.5 TEST executable from `2cc8a5a07d4305408697496a6256a412c5ce5a6d`: 51,947,631 bytes, SHA-256 `41266E96BDA8376F28090ED60A200262121B95F16FD87C78757B3B24072D065E`; separate-process startup remained responsive.
- Phase H added `V05_PHASE_H_WINDOWS_CHECKLIST.md` and expanded the three rule-schema procedures. Since the current HEAD is newer than the previous RC build, a fresh build is required for final provenance.
- Phase H RC build from `b3e930253a0b5951e98194f724a1b3cacb4899c`: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 51,947,979 bytes, SHA-256 `FE3D862F16FE2B0A2BA21DBF81352469C0D5E3FF190C525AA5A7EA6D1A4E0ACE`; separate-process startup remained responsive.
- Phase I added localized module-introduction action labels and the control inventory `V05_PHASE_I_CONTROL_INVENTORY.md`; full per-window locale cleanup and packaged click-through remain acceptance work.
- Phase I TEST build from `c590e90da66c2b57ed08a52d0d3fcc9e899f6d7e`: 51,948,592 bytes, SHA-256 `C534E9666768A4591743569BB452907C15E7FB91E20340418DEBE1AEDAF449B6`; separate-process startup remained responsive.
- Phase I.1 added direct risk-scanner file/result controls, a copyable Norwegian–Danish seven-column example, risk tutorial/manual anchors and regression coverage.
- Phase I.1 TEST build from `ffbaffc8cbd883719002f0c037661811333cef73`: 51,951,859 bytes, SHA-256 `E9AA1047087AFB8C60DE04EE3DEF7575B35FE6F257A32EF172DF7B401E4FB576`; separate-process startup remained responsive.
- Phase I.2 added shared compact result/help controls to Risk Scanner, Interference Scanner and Word Index. TEST build from `3f4bf2919acbae36dd92ca99ac0b8dbde2a33296`: 51,955,432 bytes, SHA-256 `18C799AE48CF6DB1A0605C6C311A929AC755BBCBC58E44AEDA6DCC24E375F8A8`; separate-process startup remained responsive.
- Phase I.3 repaired Prompt Library storage/UI integration, replaced Prompt Builder task IDs with Danish labels, and expanded offline manual/tutorial resources.
- Phase I.3 TEST build from `099e51cc512e725f88b5cb4a7f856b80419a2709`: 51,956,581 bytes, SHA-256 `6C967EFC86ED6309311E6A1AFC99001F45EF2A2F2A5AC4283DA28CA57C3C98CF`; separate-process startup remained responsive.
- Phase I.4 added visible built-in Prompt Library templates and the localization/documentation coverage report `V05_PHASE_I4_LOCALIZATION.md`.
- Phase I.4 TEST build from `9ecc1d8953c0737eb2cb7164bd94474eef6f07bb`: 51,957,036 bytes, SHA-256 `F827831D301C68FDB63E1A5C2C931AD7E347B1060E7985AC7C7A55525817562A`; separate-process startup remained responsive.
- Phase I.4.1 TEST build from `5feea0e4946c390d5cd7d56740f5fd9bfed3a5e4`: 51,961,602 bytes, SHA-256 `2776369D04354E404C169FE9F68B440648AB228D8E40EE0FC819ABBF11969D99`; separate-process startup remained responsive.
- Phase I.5 applied Danish navigation labels, removed the visible Phase D suffixes, and fixed export of the currently displayed prompt. TEST build from `c95196821167cbc84cf2a0c7c8290f8304964642`: 51,962,542 bytes, SHA-256 `C806631F78A36575DFB6034BB382F10ED13E8B415B4DFFE5F6E4095EEDA0973C`; separate-process startup remained responsive.
- Phase I.6 applied user-facing Danish navigation names and localized language-selector display names while preserving internal ISO codes. The final AppShell boilerplate fix is commit `9baa7cdcc007f1a6a6d6cf880ea591b277ff6320`.
- Phase I.6 TEST build from `9baa7cdcc007f1a6a6d6cf880ea591b277ff6320`: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 51,963,963 bytes, SHA-256 `29B78E9DE280C118A61FBC82C92CE6AAEA0518ED3DCC06710E1A076255C65AAF`; separate-process startup remained responsive.
- Phase I.6 automated regression suite: **76 passed, 0 failed**, with one PytestCacheWarning caused by workspace cache permissions. Full six-language secondary-window localization, packaged GUI click-through, and Microsoft Word visual acceptance remain pending and are not claimed as passed.
- Phase I.6.2 increment: runtime module-introduction refresh and localized built-in Prompt Library names were implemented. Automated suite: **77 passed, 0 failed**. Acceptance details are in `V05_PHASE_I62_ACCEPTANCE.md`; six complete manuals/tutorial sets and packaged/Word acceptance remain open.
- Phase I.6.2 TEST build from `29dd6a69bba119d09e2537752aaa1f6261de5c24`: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 51,966,000 bytes, SHA-256 `6721365D5744AFF8787F570429452170A8D0FBAEAABFE908AEF9C68C169FFB46`; separate-process startup remained responsive.
- Phase I.6.2b added Swedish, Norwegian Bokmål, German and French manual/tutorial source resources, localized manual resolution and an expanded coverage matrix. Full secondary-window localization and native linguistic approval remain open. TEST build from `252df7c698cd8275e776a0eda6f224a3d33ed769`: 51,976,532 bytes, SHA-256 `B5BA74A86A594D9B141EC8349AD45F3E0CB2FB0CA547A0E755E329D499631F79`; separate-process startup remained responsive.
- Phase I.6.2c added the shared secondary-window UI catalog and localized core controls. Full suite: **79 passed, 0 failed**. TEST build from `541b1d1d6535b5142575d3e272447885b9ce0bbb`: 51,978,448 bytes, SHA-256 `BEAF65E8DA0C7B57991418F7812424F0303FE9B6F3628C1C02D5E579B5BAA9FF`; separate-process startup remained responsive. Full interactive GUI and Microsoft Word acceptance remain NOT TESTED.
- Phase I.6.2d added six-locale fixed-string localization hooks for Risk Scanner, DA-interference, Terminology and Glossaries & Rules, plus parameterized window tests. Full suite: **80 passed, 0 failed**. TEST build from `5f2fcbd7032b25fe64cc5d3cd843d81c984b31a3`: 51,981,902 bytes, SHA-256 `39A7A9D315DD8550C93CD3A8273F4FF2D47A3219301B51246F8F0CE579533E96`; separate-process startup remained responsive. Full GUI click-through and Word acceptance remain NOT TESTED.
- Phase I.6.2e fixed AppShell navigation and context-panel labels for all six locale codes, including runtime language switching. Full suite: **83 passed, 0 failed** (PytestCacheWarning only). Source/build commit `fe2ac6ca3c6cf14ebd461b9a90a3da8b74bc1ab7`. Fresh TEST EXE: 51,987,920 bytes, SHA-256 `E0D3A01DA51807AFCF664F3AA5181A538D1B84A1C875AEC1BA2B8BA1F6AF577`; separate-process startup responsive. Packaged dashboard smoke test passed, but full six-language click-through and Microsoft Word remain NOT TESTED.
- Localization fix 1 (`0c7d5b418b6e80d97b3f3a860ab08e474b3d3f5b`) expanded the shared six-locale catalog to legacy Inventory, Rules, Terminology, Prompt Builder and related table/form controls; added visible AppShell and fixed-label regression tests. Full suite: **85 passed, 0 failed**. Fresh TEST build: 51,990,080 bytes, SHA-256 `297E7812C1DF37124D9513F5ADD9F17AC72B0E35B6E0DF7B403B3B8669744BCE`; separate-process startup responsive. Packaged Norwegian Bokmål AppShell smoke: PASS. Remaining dynamic legacy-window messages and five-locale interactive click-through are not claimed as complete.
- Phase I.6.2f (`f5551f3fa982d8f97f5e64c0882b7bf6cabb97ef`) localized dynamic scanner, project, rule-pack and Word Index messages through named message keys, with runtime-message regression coverage. Full suite: **85 passed, 0 failed**. Fresh TEST build: 51,991,720 bytes, SHA-256 `4A201BBCABF060A39BCAA41184BF02D2D52C19976226D47B0CD6C1B57220C1F5`; separate-process startup responsive. Full six-locale interactive secondary-window walkthrough and Word acceptance remain NOT TESTED.
- Phase I.6.2g (`3560b515f765205ee96ccbe024807621d1691328`) localized the remaining Terminology and Risk Scanner validation/error dialog titles and messages, including actual six-locale dialog tests. Full suite: **88 passed, 0 failed**. Fresh TEST build: 51,993,259 bytes, SHA-256 `FBE5059B8EEEFA40F6C10208452ACA7C0E7066B4E2A24974669E41158396E0B5`; separate-process startup responsive. Manual Windows and Word acceptance remain pending.
- Phase I.6.3 (`324598ea6ec60e25138bf53584a08ea4f9bc9470`) added compact pastel information cards, localized numbered on-screen guidance, module-aware right-panel context and cached module windows for field preservation across navigation. Full suite: **90 passed, 0 failed**. Fresh TEST build: 51,995,817 bytes, SHA-256 `7B5DB2A00F6EA4CEF0349E5D9B3896841DF9B2C58007C50C5A46D5D993E09043`; packaged Dashboard/Risk Scanner visual smoke passed. Full twelve-module/six-language manual walkthrough and Microsoft Word remain NOT TESTED.

## Phase I.6.3b — interaktiv trinvis vejledning

Implementeret lokalt: modulintroduktionerne åbner nu en modeless, scrollbar trinvis vejledning med Forrige/Næste, bevaret trinposition og konkrete kontrolnavne. Text Marker har seks trin, Projektworkflow har seks trin, og workflow-formularen ligger i en egen scroll-container. Der er tilføjet bundtede Text Marker-eksempler (`data/examples/textmarker_sample.docx` og `textmarker_terms.txt`).

Verifikation: `93 passed` lokalt med `QT_QPA_PLATFORM=offscreen`. Ny EXE blev bygget fra commit `3a7daee9c0575d2d6174624c60efde7404338227` med Python 3.12.14 og PyInstaller 6.11.1. Filstørrelse er 52,038,454 bytes; SHA-256 er `A0902080817556A8C938A9CE97E38EC8FF9731C4269C5AB7D0476613DD374E8B`. GUI-processen startede som separat Windows-proces; CUA kunne ikke indeksere vinduet i denne kørsel, så visuel navigation og screenshots er ikke markeret som gennemført.
## Phase I.6.3c — layout og konkrete brugerprocedurer

StepGuide viser nu konkrete eksempel- og fejlfindingstekster, lokaliseret på seks sprog. Text Marker-vejledningen har handlingerne `Vis eksempel` og `Gem eksempel som…`, der åbner eller kopierer de bundtede DOCX/TXT-eksempler. Der er tilføjet regressionstest for de seks sprogs Text Marker-vejledning.

Verifikation: `94 passed`. Ny EXE fra commit `c6b0cc1ee6a8f75b76fbb43f85a049e76365d0af`, 52,040,229 bytes, SHA-256 `51E06AD5018492A6BB04A25F16EC5FB4B769965F7B0AC6111725223206470227`. Pakket processtart er ikke visuelt navigeret i CUA; screenshots og Microsoft Word-kontrol er derfor fortsat ikke testet.
## Phase I.6.3d — layout og trin-specifik fejlfinding

Modulintroduktionerne bruger nu 12 px top/side-margin, ensartet 10 px spacing, `SetMinimumSize` og naturlig widgethøjde uden stretch. StepGuide har kompakt resizable standardstørrelse og konkrete fejlfindingstekster for Text Marker og Project Workflow.

Verifikation: `96 passed`. EXE fra commit `8167a083556b817ebb500ff610628dce787768d0`, 52,042,127 bytes, SHA-256 `2A75212189A753061D50280361A872A7C3DE52252EF1821803EE3C1422AEF817`. Pakket visuel kontrol og screenshots er ikke gennemført i CUA; Microsoft Word er ikke testet.
## Phase I.6.3e — termlisteformat og eksempler

Trin 2 i Text Marker dokumenterer nu parserens faktiske format: TXT/MD bruger én term pr. linje, mens CSV kræver `expression` og accepterer valgfrie `category`, `color` og `enabled`. Der er tilføjet `data/examples/textmarker_terms.csv` med fem gyldige termer og et detaljeret dansk tutorialsafsnit med tabel og eksempler.

Verifikation: `97 passed`. EXE fra commit `4912be5f4abdb89bd8c396973decb9733e61b8c4`, 52,044,186 bytes, SHA-256 `F76ED5E92FD2813CE8955E1F3254F522D920FCFC59BA7FA4C16B1BF069FD7E34`. Pakket GUI og Microsoft Word er ikke manuelt testet.
## Phase I.6.3g — CSV-eksempelbibliotek og lokale AI-prompts

Tilføjet fælles bibliotek med validerede eksempler for Text Marker, Translation Risk Scanner, DA-interferens, canonical rule packs og terminologi. Tilføjet offline HTML-oversigt med faktiske kolonner og en lokal prompt til CSV-generering. Der er ingen AI-upload eller API-integration.

Verifikation: `98 passed`. EXE fra commit `30bcebe`, 52,046,899 bytes, SHA-256 `05B35C2AB0B4017702EE424D1A8ECAEC718475A92F1834CB964BD67AF71E651A`. Pakket GUI er ikke manuelt gennemgået.
## Phase I.6.3h — CSV-bibliotek GUI

Tilføjet `CsvExampleLibraryWindow` med fem kort: forhåndsvisning, Gem eksempel som…, Kopiér prompt, Vis kolonner og Validér CSV. Vinduet åbnes fra Hjælp og bruger de eksisterende eksempelfiler og parserfunktioner. Ingen fil importeres automatisk, og programmet uploader ikke dokumenter.

Verifikation: `99 passed`. EXE fra commit `e78f350a9f3a06cdbc5d0b79e85a0098130f88cf`, 52,053,189 bytes, SHA-256 `8A17504447AE6E185F8CAB5DCE15D3C5BCCE4E2418B9F1CB153549A9A9D8F9A1`. Pakket GUI er ikke manuelt gennemgået.
## Phase I.6.3j — lokaliserede CSV-prompts

Årsagen til blandede sprog var faste franske beskrivelser i `_ITEMS`, som blev genbrugt af alle locales. Promptbygningen bruger nu locale-specifikke beskrivelser og afslutninger; tekniske headere og værdier er uændrede. Vis prompt og Kopiér prompt bruger samme funktion.

Verifikation: `100 passed`, inklusive 30 kombinationer (5 skemaer × 6 sprog). EXE fra commit `449d8e72b0af8ae78b18461125a771baab72b69a`, 52,054,920 bytes, SHA-256 `60D941CF7D9D0AEBD95E11AB75935777B27EBBD8D26FCF064F10C53249BF0142`. Pakket GUI er ikke manuelt testet.
## Phase I.7.1 — Text Marker layout og individuelle farver

TXT-termlister understøtter nu `udtryk%farve`; `%%` er escape for bogstaveligt procenttegn. Uden farve bruges `yellow`. CSV-kolonnen `color` fortsætter med at styre Word-fremhævningen via `TermSpec.highlight_color` og `w:highlight`. Trin 2 viser den faktiske palette dynamisk og med rigtige linjeskift.

Verifikation: `104 passed`. EXE fra commit `a20d469b7dfcc550a4df3255378e8ad0ee7b9111`, 52,056,063 bytes, SHA-256 `7D6BE44F26A91EA558CD301359EFDACC47C79F6E82B85AF4F4CC0A8E0BC14DD8`. Microsoft Word og OnlyOffice er ikke testet.

## Fase I.7.3A — fælles layout, konkrete vejledninger og eksempelfiler

Modulintroduktionerne bruger nu kompakte, indholdstilpassede kort uden `SetMinimumSize`, stretch eller faste minimumshøjder. Trinvis vejledning bruger eksplicitte modulspecifikke trin for alle 12 moduler og seks UI-sprog; de tidligere generiske fallback-tekster er ikke længere standard. Eksempelfiler kan kopieres til en bruger-valgt projektmappe via den fælles `copy_module_examples`-funktion, mens bundtede originaler forbliver uændrede. Tekst Marker, risikoscanner, interferensscanner, rule packs og terminologi har konkrete eksempelressourcer.

Automatiseret verifikation: `107 passed` (1 PytestCacheWarning om manglende skriveadgang til `.pytest_cache`). Den nye regressionsfil kontrollerer konkrete trin, seks sprog, eksempelfiler og byte-for-byte bevarelse af bundtede originaler. Ny build fra kodecommit `eb447787cbbe04654a9ebf70047251259a13d766`: `dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe`, 52.059.280 bytes, SHA-256 `65042D1BB277CE31E33E985A1DAEA7CB8779EF255F50C117EC7331EBA61A6564`. Pakket visuel GUI-kontrol, screenshots og Microsoft Word/OnlyOffice er ikke verificeret i dette miljø.
