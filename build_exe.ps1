$ErrorActionPreference = "Stop"

python -m pip install --upgrade pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name sw1sw2-ui tkinter_ui.py

Write-Host "Build finished. Output: dist/sw1sw2-ui.exe"
