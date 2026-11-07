# v0.3 testplan

Automatisér regelvalidering, alle tre kategorier, Unicode/case, false friends/shared words, deterministic rule-to-finding mapping, orange OOXML, DOCX-format/source preservation, no-overwrite, cancellation rollback og inventory registration. Kør eksisterende v0.2-regressioner uændret.

Pakket Windows-test skal åbne alle fem moduler, scanne en dansk fixture med dansk og norsk regelsæt, validere begge stopordslister i Word Index og kontrollere inventarvisning. Microsoft Word åbning uden repair warning er en manuel gate.
