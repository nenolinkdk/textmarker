$ErrorActionPreference = 'Stop'
py -3 -m pip install -e ".[gui]"
py -3 -m pip install pyinstaller
py -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name "TextMarker-0.1-TEST" --paths src src/textmarker/ui/main_window.py
Get-FileHash dist/TextMarker-0.1-TEST.exe -Algorithm SHA256
