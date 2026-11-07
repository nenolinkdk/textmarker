# Nenolink TextMarker

A local, offline Windows application for highlighting specified words and phrases in a Microsoft Word document using a user-supplied word list.

**Status:** v0.1 specification and Codex handoff. Implementation pending.

## User workflow

1. Select a source `.docx` or UTF-8 `.txt` manuscript.
2. Select a `.csv`, `.txt`, or `.md` list of terms and expressions.
3. Review/edit matching options and category colors.
4. Start processing and review the results.
5. Save a new `.docx` document and a `.csv` statistics report.

**Important:** Highlight text with Word's colored background text-highlighting feature. Do NOT use strikethrough or change text color. Never overwrite the original document.

## Specifications

- [Product requirements](docs/PRODUCT_REQUIREMENTS.md)
- [Architecture and FSM](docs/ARCHITECTURE.md)
- [Test and release plan](docs/TEST_PLAN.md)
- [Implementation phases](docs/IMPLEMENTATION_PLAN.md)
- [Instructions for Codex](AGENTS.md)
- [Example term list](examples/terms.csv)

## Development

Use Python 3.12+, PySide6, python-docx/lxml, and pytest. Package a Windows test executable with PyInstaller. See AGENTS.md for the exact definition of done.

No cloud services, AI analysis, telemetry, or transmission of manuscript content. Input and output files stay on the user's computer.

## Translation Risk Scanner v0.1

The separate `risk_gui_entry` workflow scans literal, configurable CSV risk rules in a DOCX and writes a new highlighted DOCX plus one-row-per-occurrence revision CSV. Findings are possible risks for human review only. See `docs/RISK_SCANNER_REQUIREMENTS.md`.
