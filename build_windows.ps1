$ErrorActionPreference = 'Stop'
$python = '.clean-build-venv\Scripts\python.exe'
& $python -m pip install -r build-requirements.txt
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name "TextMarker-0.1-TEST" --distpath dist-final --workpath build-final --specpath work-final --paths src src/textmarker/gui_entry.py
Get-FileHash dist-final/TextMarker-0.1-TEST.exe -Algorithm SHA256
