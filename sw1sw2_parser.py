#!/usr/bin/env python3
"""ISO/IEC 7816 SW1/SW2 parser.

Usage:
  python sw1sw2_parser.py 9000
  python sw1sw2_parser.py 6A82
  python sw1sw2_parser.py 63 C3
  echo 63C1 | python sw1sw2_parser.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Meaning:
    category: str
    description: str


# Common status words defined by ISO/IEC 7816-4 plus practical additions.
EXACT_MAP: dict[str, Meaning] = {
    "9000": Meaning("Normal processing", "Command successfully executed."),
    "6200": Meaning("Warning", "State of non-volatile memory unchanged."),
    "6281": Meaning("Warning", "Part of returned data may be corrupted."),
    "6282": Meaning("Warning", "End of file/record reached before reading Le bytes."),
    "6283": Meaning("Warning", "Selected file invalidated."),
    "6284": Meaning("Warning", "FCI not formatted according to ISO 7816-4."),
    "6300": Meaning("Warning", "State of non-volatile memory changed."),
    "6400": Meaning("Execution error", "State of non-volatile memory unchanged."),
    "6581": Meaning("Execution error", "Memory failure."),
    "6700": Meaning("Checking error", "Wrong length."),
    "6881": Meaning("Checking error", "Logical channel not supported."),
    "6882": Meaning("Checking error", "Secure messaging not supported."),
    "6883": Meaning("Checking error", "Last command of chain expected."),
    "6884": Meaning("Checking error", "Command chaining not supported."),
    "6981": Meaning("Checking error", "Command incompatible with file structure."),
    "6982": Meaning("Checking error", "Security status not satisfied."),
    "6983": Meaning("Checking error", "Authentication method blocked."),
    "6984": Meaning("Checking error", "Referenced data invalidated."),
    "6985": Meaning("Checking error", "Conditions of use not satisfied."),
    "6986": Meaning("Checking error", "Command not allowed (no current EF)."),
    "6987": Meaning("Checking error", "Expected secure messaging object missing."),
    "6988": Meaning("Checking error", "Secure messaging data object incorrect."),
    "6A80": Meaning("Checking error", "Incorrect parameters in data field."),
    "6A81": Meaning("Checking error", "Function not supported."),
    "6A82": Meaning("Checking error", "File or application not found."),
    "6A83": Meaning("Checking error", "Record not found."),
    "6A84": Meaning("Checking error", "Not enough memory space."),
    "6A85": Meaning("Checking error", "Lc inconsistent with TLV structure."),
    "6A86": Meaning("Checking error", "Incorrect P1/P2 parameter."),
    "6A87": Meaning("Checking error", "Lc inconsistent with P1/P2."),
    "6A88": Meaning("Checking error", "Referenced data not found."),
    "6B00": Meaning("Checking error", "Wrong parameters P1/P2."),
    "6D00": Meaning("Checking error", "Instruction code (INS) not supported."),
    "6E00": Meaning("Checking error", "Class not supported."),
    "6F00": Meaning("Checking error", "No precise diagnosis; command aborted."),
}


def normalize(raw: str) -> str:
    no_prefix = re.sub(r"0x", "", raw, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^0-9a-fA-F]", "", no_prefix).upper()
    if len(cleaned) != 4:
        raise ValueError("SW1SW2 must contain exactly 2 bytes (4 hex chars), e.g. 9000 or 6A82")
    return cleaned


def parse_status(sw: str) -> Meaning:
    if sw in EXACT_MAP:
        return EXACT_MAP[sw]

    sw1 = sw[:2]
    sw2 = int(sw[2:], 16)

    if sw1 == "61":
        return Meaning("Normal processing", f"{sw2} response byte(s) still available (issue GET RESPONSE).")
    if sw1 == "62":
        return Meaning("Warning", "State of non-volatile memory unchanged.")
    if sw1 == "63":
        if (sw2 & 0xF0) == 0xC0:
            retries_left = sw2 & 0x0F
            return Meaning("Warning", f"Verification failed; {retries_left} retry(ies) remaining.")
        return Meaning("Warning", "State of non-volatile memory changed.")
    if sw1 == "64":
        return Meaning("Execution error", "State of non-volatile memory unchanged.")
    if sw1 == "65":
        return Meaning("Execution error", "State of non-volatile memory changed.")
    if sw1 == "66":
        return Meaning("Security error", "Security-related status (implementation-specific).")
    if sw1 == "67":
        return Meaning("Checking error", "Wrong length.")
    if sw1 == "69":
        return Meaning("Checking error", "Command not allowed / security condition not satisfied.")
    if sw1 == "6A":
        return Meaning("Checking error", "Wrong parameter(s) P1/P2 or data field issue.")
    if sw1 == "6C":
        return Meaning("Checking error", f"Wrong Le. Correct Le is {sw2} (0x{sw[2:]}).")

    return Meaning("Unknown", "Status word not in current ISO 7816 quick map (may be proprietary).")


def parse_input(argv: list[str]) -> str:
    if len(argv) >= 3:
        return "".join(argv[1:3])
    if len(argv) == 2:
        return argv[1]
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise ValueError("Usage: python sw1sw2_parser.py <SW1SW2> OR <SW1> <SW2>")


def main(argv: list[str]) -> int:
    try:
        raw = parse_input(argv)
        sw = normalize(raw)
        meaning = parse_status(sw)
    except ValueError as exc:
        print(f"Input error: {exc}")
        return 2

    print(f"SW1SW2: {sw}")
    print(f"Category: {meaning.category}")
    print(f"Meaning: {meaning.description}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
