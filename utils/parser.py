\
from __future__ import annotations

import base64
import re
from typing import Iterable


ADDRESS_RE = re.compile(r"^(?:0|[-]1):[0-9a-fA-F]{64}$")
HEX_RE = re.compile(r"^[0-9a-fA-F]{64}$")
WALLET_NAME_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def is_address(value: str) -> bool:
    return bool(ADDRESS_RE.match(value.strip()))


def normalize_address(value: str) -> str:
    value = value.strip()
    if HEX_RE.match(value):
        return f"0:{value.lower()}"
    return value


def decode_b64_bytes(data: str | None) -> bytes:
    if not data:
        return b""
    try:
        return base64.b64decode(data + "===")
    except Exception:
        return b""


def ascii_candidates(blob: bytes) -> list[str]:
    # Extract printable ASCII fragments from a raw BOC / cell payload.
    text = blob.decode("latin1", errors="ignore")
    candidates = re.findall(r"[A-Za-z0-9][A-Za-z0-9 _./:@+-]{2,64}", text)
    # Keep only fragments that look like names or labels.
    cleaned: list[str] = []
    for c in candidates:
        c = c.strip("\x00\t\r\n ")
        if len(c) < 3:
            continue
        if c.upper() in {"HTTP", "HTTPS", "JSON", "CELL", "BOC", "ABI"}:
            continue
        cleaned.append(c)
    return cleaned


def guess_wallet_name(data_b64: str | None) -> str | None:
    blob = decode_b64_bytes(data_b64)
    if not blob:
        return None
    cands = ascii_candidates(blob)
    # Prefer shorter alnum names near the end of the BOC.
    for cand in reversed(cands):
        if 2 <= len(cand) <= 32 and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{1,31}", cand):
            return cand
    return cands[-1] if cands else None


def format_units(raw: str | int | None, decimals: int = 9, precision: int = 4) -> str:
    if raw is None:
        return "0"
    try:
        n = int(str(raw))
    except Exception:
        return str(raw)
    sign = "-" if n < 0 else ""
    n = abs(n)
    whole = n // (10**decimals)
    frac = n % (10**decimals)
    if precision <= 0:
        return f"{sign}{whole}"
    frac_str = f"{frac:0{decimals}d}"[:precision].rstrip("0")
    return f"{sign}{whole}" if not frac_str else f"{sign}{whole}.{frac_str}"


def human_amount(value: int | str | None, decimals: int = 9, precision: int = 2) -> str:
    if value is None:
        return "0"
    try:
        n = int(str(value))
    except Exception:
        return str(value)
    whole = n // (10**decimals)
    frac = n % (10**decimals)
    frac_str = f"{frac:0{decimals}d}"[:precision].rstrip("0")
    return f"{whole:,}" if not frac_str else f"{whole:,}.{frac_str}"


def join_lines(lines: Iterable[str]) -> str:
    return "\n".join(lines)
