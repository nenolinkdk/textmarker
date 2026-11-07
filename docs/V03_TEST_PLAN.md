# v0.3 testplan

Automatisér regelvalidering, alle tre kategorier, Unicode/case, false friends/shared words, deterministic rule-to-finding mapping, orange OOXML, DOCX-format/source preservation, no-overwrite, cancellation rollback og inventory registration. Kør eksisterende v0.2-regressioner uændret.

Phase B automation: `tests/test_da_interference.py` verifies strict schema, three classifications, source hash preservation, `w:shd`/`w:highlight`, occurrence CSV, summary CSV, no-overwrite and pre-cancel cleanup. Manual Word rendering remains a later acceptance gate.

Pakket Windows-test skal åbne alle fem moduler, scanne en dansk fixture med dansk og norsk regelsæt, validere begge stopordslister i Word Index og kontrollere inventarvisning. Microsoft Word åbning uden repair warning er en manuel gate.
