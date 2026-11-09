$ErrorActionPreference='Stop'
$python='.clean-build-venv\Scripts\python.exe'
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name 'Nenolink-Text-Tools-0.4-TEST-hotfix' --distpath dist-text-tools-0.4-hotfix --workpath build-text-tools-0.4-hotfix --specpath . --paths src --add-data "data;data" --add-data "src/textmarker/multilingual/locales;textmarker/multilingual/locales" --add-data "docs/manual;docs/manual" src/textmarker/text_tools_gui_entry.py
Get-FileHash dist-text-tools-0.4-hotfix/Nenolink-Text-Tools-0.4-TEST-hotfix.exe -Algorithm SHA256
