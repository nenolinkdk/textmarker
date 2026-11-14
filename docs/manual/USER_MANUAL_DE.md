# Nenolink Text Tools v0.5 – Benutzerhandbuch

Diese Offline-Anleitung beschreibt die lokale Übersetzungsprüfung. Die Oberflächensprache sowie Quell- und Zielsprache werden unabhängig gespeichert.

## Dateien und Regeln

Text Marker verarbeitet DOCX/TXT mit einer CSV-, MD- oder TXT-Ausdrucksliste. Der Translation Risk Scanner verlangt `expression,category,color,severity,explanation,suggestion,enabled` und erzeugt eine markierte DOCX sowie occurrence- und optionale summary-CSV. Der Language Interference Scanner verlangt `rule_id,expression,language,category,severity,color,explanation,suggestion,enabled`. Canonical Rule Packs besitzen elf eigene Spalten; Formate dürfen nicht vermischt werden. UTF-8 und der erkannte CSV-Trenner werden verwendet. Ausgaben werden separat veröffentlicht, die Quelle bleibt unverändert.

## Module und Interpretation

Dashboard und Project Workflow verbinden Projekt, Sprachpaar, Arbeitsordner, Rule Packs und Dokument. Translation Risk Scanner markiert mögliche falsche Freunde und irreführende Ähnlichkeiten verwandter Sprachen; ein Treffer ist kein bestätigter Fehler. Language Interference Scanner liefert RED/ORANGE/YELLOW-Kandidaten, wobei gemeinsame skandinavische Wörter durchaus korrekt sein können. Word Index zählt Wörter aus DOCX/TXT mit optionalen dänischen oder norwegischen Stoppwörtern und exportiert CSV/TXT für Terminologie- und Interferenzprüfung.

File Inventory speichert lokale Pfade und kennzeichnet fehlende Dateien. Terminology verwaltet Konzepte, mehrsprachige Terme, Status und CSV-Mappings in SQLite; Dubletten werden nur angezeigt. Glossaries & Rules importiert, validiert, bearbeitet und exportiert Rule Packs. Prompt Library und Prompt Builder erzeugen lokale, editierbare Review-Prompts ohne Cloud-Dienst. Settings speichert Sprache, Projekt und Ordner; Help öffnet passende Offline-Anker.

## Tutorials

1. Norsk→Dänisch: Risk Scanner öffnen, norwegische DOCX und `data/examples/risk_rules_no_da.csv` wählen, Ausgabe angeben, scannen und jeden Treffer im Kontext der dänischen Übersetzung prüfen.
2. Interferenz: neun-spaltige Regeldatei wählen, Kategorien filtern, scan ausführen und Erklärung/Suggestion lesen; Kandidat und Fehler nicht verwechseln.
3. Word Index: Sprache `nb` oder `da`, Stoppwörter an/aus, CSV/TXT exportieren und häufige Wörter als Terminologie-Kandidaten prüfen.
4. Terminology: Konzept und Terme in zwei Sprachen anlegen, Status setzen, Kunden-CSV mappen, Dubletten prüfen und canonical CSV exportieren.
5. Text Marker: separates DOCX und Ausdrucksliste wählen, starten und das neue DOCX öffnen; niemals über die Quelle speichern.
6. Regeldatei: Beispiel kopieren, exakte Header behalten, UTF-8 speichern und Validierungsfehler vor dem Scan beheben.
7. Prompt Library/Builder: Template, `nb`→`da`, Genre und Kriterien wählen, Preview bearbeiten, persönliche Kopie speichern und TXT exportieren.

## Grenzen

Ungültige oder gemischte CSV-Schemata werden abgelehnt. Automatische Treffer müssen linguistisch geprüft werden. Die Word-Reparatur- und Formatprüfung ist ein manueller Akzeptanzschritt.
Text-Marker-Farben: TXT kann `Ausdruck%Farbe` verwenden, CSV die Spalte `color`. Ohne Farbe wird `yellow` verwendet. Für ein wörtliches Prozentzeichen verwenden Sie `%%`.
