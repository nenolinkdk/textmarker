$ErrorActionPreference = 'Stop'
$python = '.clean-build-venv\Scripts\python.exe'
& $python -m pip install -r build-requirements.txt
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name "TextMarker-0.1-TEST" --paths src --collect-all PySide6 --collect-all shiboken6 src/textmarker/gui_entry.py
Get-FileHash dist/TextMarker-0.1-TEST.exe -Algorithm SHA256
