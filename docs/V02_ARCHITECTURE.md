# v0.2 architecture

The shared launcher owns navigation only. Each module owns its view model and worker, while reusable processing services remain independent:

`Launcher -> ModuleHost -> {TextMarkerAdapter, RiskScannerAdapter, WordIndexController, InventoryController}`

Workers communicate progress/results/cancellation through Qt signals. DOCX safety and matching reuse the existing highlighter/matcher. Word Index exposes `index_docx(source, language, stopwords)` and exporters. Inventory uses SQLite with migrations and parameterized queries; it stores paths and metadata, never contents.

The launcher never duplicates processing state. A module can fail or be unavailable without taking down the home screen.
# Technical corrections

- Stopword resources are resolved through `resource_path()`, which selects the PyInstaller `_MEIPASS` bundle or the source-tree `data/` directory.
- Word Index exposes optional reference-only inventory registration in the GUI; it stores metadata in `~/.nenolink/file_inventory.sqlite` and never modifies the source.
- Worker cancellation is cooperative through `threading.Event`; the window close handler requests cancellation, waits for the worker and then accepts close.
- DOCX extraction reads `word/document.xml`, including body paragraphs nested in tables. Paragraphs with unsupported run children are skipped and reported as warnings; no XML mutation occurs.
