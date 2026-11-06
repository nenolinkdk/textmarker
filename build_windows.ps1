$ErrorActionPreference = 'Stop'
py -3 -m pip install -e ".[gui]"
py -3 -m pip install pyinstaller
py -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name TextMarker_TEST src/textmarker/__main__.py
Get-FileHash dist/TextMarker_TEST.exe -Algorithm SHA256
