# SW1SW2 Quick Parser

A tiny CLI tool to parse APDU status words (SW1/SW2) using a practical ISO/IEC 7816 quick map.

## Usage

```bash
python sw1sw2_parser.py 9000
python sw1sw2_parser.py 6A82
python sw1sw2_parser.py 63 C3
```

## Example output

```text
SW1SW2: 6A82
Category: Checking error
Meaning: File or application not found.
```

> Note: Some cards return proprietary status words; those are reported as `Unknown`.
