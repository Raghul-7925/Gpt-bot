\
from __future__ import annotations

from typing import Any

import json
from pathlib import Path

from config import settings
from decoder import WalletReport, decode_wallet_info
from graphql import GraphQLClient
from utils.parser import is_address, normalize_address


class WalletService:
    def __init__(self, client: GraphQLClient):
        self.client = client
        self.aliases = self._load_aliases()

    def _load_aliases(self) -> dict[str, str]:
        p = settings.aliases_path
        if not p.exists():
            return {}
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            return {str(k).strip().lower(): normalize_address(str(v).strip()) for k, v in raw.items()}
        except Exception:
            return {}

    async def resolve_input(self, raw: str) -> str:
        value = raw.strip()
        value = normalize_address(value)
        if is_address(value):
            return value
        alias = self.aliases.get(value.lower())
        if alias:
            return alias
        raise ValueError(
            "Name resolution is not wired for unknown names in this MVP. Use a wallet address or add the name to aliases.json."
        )

    async def get_wallet_report(self, raw: str) -> WalletReport:
        account_id = await self.resolve_input(raw)
        account_info = await self.client.get_account_snapshot(account_id)
        indexer_data = None

        # Best effort: if the wallet is an indexer/multifactor-like account, try to pull the linked name data.
        try:
            indexer_data = await self.client.get_indexer_data(account_id)
        except Exception:
            indexer_data = account_info.get("data")

        report = decode_wallet_info(raw.strip(), account_id, account_info, indexer_data)
        return report
