# v0.3 testplan

Automatisér regelvalidering, alle tre kategorier, Unicode/case, false friends/shared words, deterministic rule-to-finding mapping, orange OOXML, DOCX-format/source preservation, no-overwrite, cancellation rollback og inventory registration. Kør eksisterende v0.2-regressioner uændret.

Phase B automation: `tests/test_da_interference.py` verifies strict schema, three classifications, source hash preservation, `w:shd`/`w:highlight`, occurrence CSV, summary CSV, no-overwrite and pre-cancel cleanup. Manual Word rendering remains a later acceptance gate.

Phase C automation: launcher route count, DA window controls, worker cancellation state, repeated findings, overlap, Unicode, run formatting and full v0.2 regression suite. Packaged GUI and Microsoft Word opening remain Windows acceptance tests.

Pakket Windows-test skal åbne alle fem moduler, scanne en dansk fixture med dansk og norsk regelsæt, validere begge stopordslister i Word Index og kontrollere inventarvisning. Microsoft Word åbning uden repair warning er en manuel gate.
