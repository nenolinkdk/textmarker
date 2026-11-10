# v0.5 Phase G acceptance

Statuses are limited to PASS, FAIL, BLOCKED and NOT TESTED.

| Area | Status | Evidence |
|---|---|---|
| Branch and baseline | PASS | `feature/text-tools-v0.5`, baseline `cb311617928e83e7644ec392d2aa7b6e2dfec169` |
| Automated regression suite | PASS | 68 passed, 0 failed; one cache-permission warning |
| GitHub push | BLOCKED | `fatal: unable to access 'https://github.com/nenolinkdk/textmarker.git/': Failed to connect to github.com:443 after 109 ms` |
| Translation Risk CSV audit | PASS | Exact seven required columns; UTF-8/BOM; comma/semicolon; generated IDs |
| DA-interference CSV audit | PASS | Exact nine required columns; strict language/category/severity/color validation |
| Canonical v0.4 rule-pack audit | PASS | Eleven documented columns and explicit legacy adapters |
| Bundled DA example | PASS | `data/examples/da_interference_rules.csv` loads with DA parser |
| Offline help IDs/anchors | PASS | Module links resolve; `scanner.rules`, `interference.rules` and `tutorial.overview` present |
| Packaged startup | PASS | Existing v0.5 executable starts as a separate process and remains responsive |
| Release-candidate build | PASS | PyInstaller 6.11.1 / Python 3.12.14; built from commit `830f4118e90d89e7ea0a84a16d4d316d63e26403`; 51,943,095 bytes; SHA-256 `DE5B5B1DFB3904B0D8F8A0A0FACCC6B9DD61FDA7E08A2BAE5487F1B5DF98F22C` |
| Packaged Terminology round trip | NOT TESTED | Desktop GUI click-through unavailable in this session |
| Packaged Prompt Builder | NOT TESTED | Desktop GUI click-through unavailable in this session |
| Packaged help click-through | NOT TESTED | Process startup was observable; individual clicks were not |
| DOCX scanner acceptance | NOT TESTED | Representative documents prepared by prior phases; no Word session available here |
| Microsoft Word repair/visual check | NOT TESTED | Must be opened manually in Microsoft Word |

## Manual Word procedure

Open representative outputs from Text Marker, Translation Risk Scanner and Language Interference Scanner in Microsoft Word. Confirm no repair dialog, unchanged text and existing formatting, tables, highlights and tracked changes preserved; confirm only intended `w:highlight`/`w:shd` markings are added. Record each document and result before release consideration.

Release remains blocked until the NOT TESTED packaged workflows and Microsoft Word checks are completed.
