# Nenolink Text Tools v0.2 requirements

## Acceptance criteria

- One offline Danish PySide6 launcher exposes Text Marker, Translation Risk Scanner and Word Index without changing legacy entry points.
- Word Index reads DOCX body/table text, reports unsupported OOXML, supports Danish and Norwegian Bokmål tokenization, language-specific editable 100-word stopword resources, frequency counts, deterministic A–Z/Æ/Ø/Å ordering, UTF-8 BOM CSV and UTF-8 TXT export, progress/cancel and fail-closed output paths.
- File Inventory stores references only in local SQLite, with role/type/language/size/mtime/module/last-used metadata; it can register, search/sort, open, reuse and remove references without deleting files and survives restart.
- Existing TextMarker and Risk Scanner behavior/tests remain green.
- No source document is modified, uploaded, silently overwritten or silently deleted.

## Scope limits

No semantic translation comparison, lemmatization, automatic correction, AI, recursive disk scanning or cloud synchronization. Unsupported OOXML is warned/skipped, never reported as clean.
