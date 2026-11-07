# Risk Scanner architecture

`risk.rules` parses validated `RiskRule` records. `risk.scanner` reuses the existing Unicode-safe matcher and OOXML highlighter, collecting occurrence locators and context before atomic highlighting. `risk.report` writes one row per occurrence. `risk_gui_entry.py` is a separate Danish GUI entry point and does not alter the TextMarker GUI or CLI.

Safe OOXML handling is fail-closed: paragraphs with unsupported run children are skipped and reported as warnings rather than flattened or rewritten. Locators currently use `body/p[n]`; they are stable within the scanned document version but are not Word bookmark identifiers.
