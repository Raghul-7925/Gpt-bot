from __future__ import annotations

from typing import Any

from config import settings
from services.graphql import GraphQLClient


class WalletService:

    def __init__(self, gql: GraphQLClient):
        self.gql = gql

    @staticmethod
    def _currency_map(balance_other: list[dict[str, Any]]) -> dict[int, float]:

        result: dict[int, float] = {}

        for item in balance_other:

            try:
                key = int(item["currency"])
                value = float(item["value"])

                result[key] = value

            except Exception:
                continue

        return result

    async def get_wallet(self, address: str) -> dict[str, Any]:

        info = await self.gql.get_account(address)

        currencies = self._currency_map(
            info.get("balance_other", [])
        )

        return {

            "address": address,

            "native_balance": float(
                info.get("balance", 0)
            ),

            "nackl": currencies.get(1, 0),

            "locked": currencies.get(2, 0),

            "usdc": currencies.get(3, 0),

            "shell": currencies.get(0, 0),

            # These will be decoded later
            "speed": None,

            "taps": None,

            "mbi": None,

            "account_type": info.get("acc_type_name"),

            "code_hash": info.get("code_hash"),

            "init_code_hash": info.get("init_code_hash"),

            "last_paid": info.get("last_paid"),

            "last_transaction": info.get(
                "last_trans_lt"
            ),

            "raw_data": info.get("data"),

            "raw_boc": info.get("boc"),
        }

    async def exists(self, address: str) -> bool:

        try:
            await self.gql.get_account(address)
            return True

        except Exception:
            return False
