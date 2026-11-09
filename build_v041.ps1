$ErrorActionPreference='Stop'
$python='.clean-build-venv\Scripts\python.exe'
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name 'Nenolink-Text-Tools-0.4.1-TEST' --distpath dist-text-tools-0.4.1 --workpath build-text-tools-0.4.1 --specpath . --paths src --add-data "data;data" --add-data "src/textmarker/multilingual/locales;textmarker/multilingual/locales" --add-data "docs/manual;docs/manual" src/textmarker/text_tools_gui_entry.py
Get-FileHash dist-text-tools-0.4.1/Nenolink-Text-Tools-0.4.1-TEST.exe -Algorithm SHA256
