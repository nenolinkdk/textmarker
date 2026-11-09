# v0.4 Windows acceptance

- [ ] Ren Python 3.12/PySide6/PyInstaller build af `Nenolink-Text-Tools-0.4-TEST.exe`.
- [ ] Navigation og alle eksisterende moduler fungerer uden datatab.
- [ ] Alle seks UI-sprog kan vælges; fallback og missing-key report er korrekt.
- [ ] Project profile gemmes, genåbnes og validerer directories.
- [ ] Legacy rules og canonical rule packs importeres uden tavs reinterpretation.
- [ ] DOCX outputs åbnes i Microsoft Word uden repair warning.
- [ ] Ingen telemetry eller dokument-upload observeres under test.
- [ ] Ambiguous/unsupported CSV schemas afvises med klar fejl.
- [ ] Project scan afviser missing/incompatible active packs før output-publicering.
- [ ] Run packaged end-to-end project workflow through scan and reports.
- [ ] Open representative DOCX outputs in Microsoft Word and record repair-warning result.

## P0 hotfix evidence

- [x] Fresh onefile hotfix EXE built with Python 3.12 and PyInstaller 6.11.1.
- [x] Main window launched from the packaged EXE without a Python traceback.
- [x] Navigation list and Settings route verified in the packaged GUI.
- [ ] Select and visually review all six UI languages on Windows.
- [ ] Open representative DOCX outputs in Microsoft Word and confirm no repair warning.
