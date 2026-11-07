# v0.2 architecture

The shared launcher owns navigation only. Each module owns its view model and worker, while reusable processing services remain independent:

`Launcher -> ModuleHost -> {TextMarkerAdapter, RiskScannerAdapter, WordIndexController, InventoryController}`

Workers communicate progress/results/cancellation through Qt signals. DOCX safety and matching reuse the existing highlighter/matcher. Word Index exposes `index_docx(source, language, stopwords)` and exporters. Inventory uses SQLite with migrations and parameterized queries; it stores paths and metadata, never contents.

The launcher never duplicates processing state. A module can fail or be unavailable without taking down the home screen.
