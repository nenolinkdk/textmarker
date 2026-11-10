# v0.5 documentation coverage matrix

This matrix distinguishes content coverage from packaged click-through testing. `PASS` means the source resource exists and matches the implemented workflow; `NOT TESTED` means the packaged Windows link still requires manual verification.

| Module | Prose complete | Input/output accurate | Guide section | Tutorial | Example data | Packaged link | Linguistic review |
|---|---|---|---|---|---|---|---|
| Dashboard | PASS | PASS | PASS (`dashboard.overview`) | PASS (first-run tutorial) | NOT TESTED | NOT TESTED | NOT TESTED |
| Project Workflow | PASS | PASS | PASS (`projects.create`) | PASS (first-run tutorial) | NOT TESTED | NOT TESTED | NOT TESTED |
| Text Marker | PASS | PASS | PASS (`textmarker.overview`, `scanner.run`) | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| Translation Risk Scanner | PASS | PASS | PASS (`scanner.overview`, `scanner.rules`, `scanner.run`) | NOT TESTED | PASS (rule schema documented) | NOT TESTED | NOT TESTED |
| Language Interference Scanner | PASS | PASS | PASS (`interference.overview`, `interference.rules`, `scanner.run`) | NOT TESTED | PASS (`data/examples/da_interference_rules.csv`) | NOT TESTED | NOT TESTED |
| Word Index | PASS | PASS | PASS (`wordindex.overview`, `wordindex.interference`) | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| File Inventory | PASS | PASS | PASS (`inventory.overview`) | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| Terminology | PASS | PASS | PASS (`terminology.overview`, `terminology.csv-import`, `terminology.csv-export`) | PASS (first-run tutorial) | NOT TESTED | NOT TESTED | NOT TESTED |
| Glossaries & Rules | PASS | PASS | PASS (`rules.overview`) | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| Prompt Library | PASS | PASS | PASS (`prompts.overview`, `prompts.builder`) | PASS (Prompt Builder) | PASS (bundled templates) | NOT TESTED | NOT TESTED |
| Settings | PASS | PASS | PASS (`settings.overview`) | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| Help | PASS | PASS | PASS (`help.overview`) | PASS (first-run tutorial) | PASS (offline help) | NOT TESTED | NOT TESTED |

The two primary UI locales (Danish and English) now contain module-specific input, processing, output and linguistic-use prose. Swedish, Norwegian Bokmål, German and French retain localized baseline copy and require native linguistic review before release. No tutorial button is presented for modules without an implemented tutorial route.
