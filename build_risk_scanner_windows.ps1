$ErrorActionPreference='Stop'
$python='.clean-build-venv\Scripts\python.exe'
& $python -m pip install -r build-requirements.txt
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name 'Nenolink-Translation-Risk-Scanner-0.1-TEST' --distpath dist-risk --workpath build-risk --specpath work-risk --paths src src/textmarker/risk_gui_entry.py
Get-FileHash dist-risk/Nenolink-Translation-Risk-Scanner-0.1-TEST.exe -Algorithm SHA256
