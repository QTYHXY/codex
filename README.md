# SW1SW2 Quick Parser

A tiny toolkit to parse APDU status words (SW1/SW2) using a practical ISO/IEC 7816 quick map.

## CLI Usage

```bash
python sw1sw2_parser.py 9000
python sw1sw2_parser.py 6A82
python sw1sw2_parser.py 63 C3
echo 63C1 | python sw1sw2_parser.py
```

## Desktop UI（基于 Python 标准库 Tkinter）

```bash
python tkinter_ui.py
```

UI features:
- Directly built with Python standard library `tkinter` (no browser framework needed).
- A modern dark-themed desktop window.
- Input accepts `9000`, `6A82`, `63 C2`, `0x6A 0x82`.
- Press Enter or click **解析** to decode.
- **清空** button for quick reset.

## Build EXE (Windows)

Option 1 (PowerShell):

```powershell
./build_exe.ps1
```

Option 2 (Git Bash / WSL shell):

```bash
./build_exe.sh
```

After success, you will get:

```text
dist/sw1sw2-ui.exe
```

## Example output

```text
SW1SW2: 6A82
Category: Checking error
Meaning: File or application not found.
```

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

> Note: Some cards return proprietary status words; those are reported as `Unknown`.
