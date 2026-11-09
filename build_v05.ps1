$ErrorActionPreference='Stop'
$python='.clean-build-venv\Scripts\python.exe'
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name 'Nenolink-Text-Tools-0.5-TEST' --distpath dist-text-tools-0.5 --workpath build-text-tools-0.5 --specpath . --paths src --add-data "data;data" --add-data "src/textmarker/multilingual/locales;textmarker/multilingual/locales" --add-data "docs/manual;docs/manual" src/textmarker/text_tools_gui_entry.py
Get-FileHash dist-text-tools-0.5/Nenolink-Text-Tools-0.5-TEST.exe -Algorithm SHA256
