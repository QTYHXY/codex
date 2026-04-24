#!/usr/bin/env bash
set -euo pipefail

# Build single-file Windows executable via PyInstaller.
# Run on Windows or in a Windows-compatible environment.

python -m pip install --upgrade pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name sw1sw2-ui tkinter_ui.py

echo "Build finished. Output: dist/sw1sw2-ui.exe"
