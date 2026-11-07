# v0.2 changelog

## Unreleased

- Design phase started for shared Text Tools launcher, Word Index and local File Inventory.
- No application behavior changed in Phase A.
- Phase B: added shared `Nenolink Text Tools v0.2` launcher with separate Text Marker, Translation Risk Scanner and Word Index routes; legacy standalone entry points remain unchanged.
# v0.2 Phase C

- Added Word Index core and Danish/Norwegian stopword resources.
- Added Danish Word Index GUI route with worker-thread processing, cancellation, progress and safe CSV/TXT output.
- Added Unicode, stopword, export and cancellation regression coverage.
- Added persistent local SQLite file inventory with SHA-256 reference metadata.
- Built and manually opened the packaged shared launcher and Word Index window.
- Review corrections: PyInstaller-aware stopword paths, GUI inventory registration, close-time worker cancellation, and regression tests for these boundaries.

