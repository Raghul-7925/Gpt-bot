\
from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any

from utils.parser import decode_b64_bytes, guess_wallet_name, human_amount


@dataclass
class WalletReport:
    query: str
    display_name: str
    wallet_address: str
    shell: str = "0"
    nackl: str = "0"
    locked: str = "0"
    usdc: str = "0"
    speed: str = "0.00"
    total_taps: str = "0"
    mbi_level: str = "0"
    extra_note: str = ""


def _find_currency_value(balance_other: list[dict[str, Any]], currency_id: int) -> str | None:
    for item in balance_other or []:
        try:
            if int(item.get("currency")) == currency_id:
                return str(item.get("value"))
        except Exception:
            continue
    return None


def decode_wallet_info(
    query: str,
    wallet_address: str,
    account_info: dict[str, Any],
    indexer_data_b64: str | None = None,
) -> WalletReport:
    balance_other = account_info.get("balance_other") or []
    shell_raw = account_info.get("balance")
    # Best effort, based on the explorer's current UI convention.
    shell = human_amount(shell_raw, decimals=9, precision=4)

    # Currency ids are best-effort defaults; if the chain changes, update them here.
    nackl = human_amount(_find_currency_value(balance_other, 1), decimals=9, precision=2)
    locked = human_amount(_find_currency_value(balance_other, 2), decimals=9, precision=2)
    usdc = human_amount(_find_currency_value(balance_other, 3), decimals=6, precision=2)

    display_name = guess_wallet_name(indexer_data_b64) or guess_wallet_name(account_info.get("data")) or query

    # The public explorer derives these from contract-specific decoding. This MVP keeps them visible
    # and makes the data model easy to upgrade later.
    speed = "0.00"
    total_taps = "0"
    mbi_level = "0"

    return WalletReport(
        query=query,
        display_name=display_name,
        wallet_address=wallet_address,
        shell=shell,
        nackl=nackl,
        locked=locked,
        usdc=usdc,
        speed=speed,
        total_taps=total_taps,
        mbi_level=mbi_level,
    )
