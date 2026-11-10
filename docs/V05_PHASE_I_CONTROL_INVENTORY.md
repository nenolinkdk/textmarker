# Phase I UI control inventory

| Navigation item | Primary action | State/availability | Status |
|---|---|---|---|
| Dashboard | Open project/module | Always available | PASS |
| Project Workflow | Choose DOCX, import/activate packs, scan, open outputs | Scan requires valid project/input | PASS |
| Text Marker | Open module and choose DOCX/TXT, list and output | Start requires selected files | PASS |
| Translation Risk Scanner | Open module and choose document/rules/output | Start requires matching risk CSV | PASS |
| Language Interference Scanner | Open module and choose DOCX/CSV/output | Start requires matching DA CSV | PASS |
| Word Index | Open module, choose DOCX, language, stopwords and export | Run requires input/output | PASS |
| File Inventory | Search, open, reuse and remove reference | Missing paths remain visible | PASS |
| Terminology | Create concept, import/map/export CSV | Destructive actions require confirmation | PASS |
| Glossaries & Rules | Import, search, enable/disable and assign packs | Invalid schema rejected | PASS |
| Prompt Library | Build, edit, save and copy prompt | Local-only persistence | PASS |
| Settings | Select UI/source/target languages and save project | Languages remain independent | PASS |
| Help | Open offline manual/tutorial | Packaged click-through pending | NOT TESTED |

The module introduction has a connected Open module action for functional routes. Native file dialogs and processing controls remain in the existing module windows and reuse their existing engines. Pakket click-through and manual Word checks are recorded separately in `V05_PHASE_H_WINDOWS_CHECKLIST.md`.
