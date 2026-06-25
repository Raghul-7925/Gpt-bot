\
from __future__ import annotations

import json
from typing import Any

import httpx


class GraphQLClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(20.0, connect=10.0),
            headers={
                "accept": "application/json, text/plain, */*",
                "content-type": "text/plain",
                "origin": "https://acki.live",
                "referer": "https://acki.live/",
                "user-agent": "Mozilla/5.0 (compatible; AckiWalletBot/1.0)",
            },
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def query(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        resp = await self._client.post(
            self.endpoint,
            content=json.dumps({"query": query, "variables": variables}),
        )
        resp.raise_for_status()
        payload = resp.json()
        if "errors" in payload and payload["errors"]:
            message = payload["errors"][0].get("message", "GraphQL error")
            raise RuntimeError(message)
        return payload["data"]

    async def get_account_snapshot(self, account_id: str) -> dict[str, Any]:
        q = """
        query GetAccountSnapshot($accountId: String!, $dappId: String!) {
          blockchain {
            account(account_id: $accountId, dapp_id: $dappId) {
              info {
                balance(format: DEC)
                balance_other { currency value(format: DEC) }
                last_paid
                last_trans_lt(format: DEC)
                code_hash
                init_code_hash
                data
                boc
                acc_type
                acc_type_name
                dapp_id
              }
            }
          }
        }
        """
        data = await self.query(q, {"accountId": account_id, "dappId": account_id})
        return data["blockchain"]["account"]["info"]

    async def get_latest_account_activity(self, account_id: str) -> dict[str, Any]:
        q = """
        query GetLatestAccountActivity($accountId: String!, $dappId: String!) {
          blockchain {
            account(account_id: $accountId, dapp_id: $dappId) {
              info {
                balance(format: DEC)
                last_paid
                last_trans_lt(format: DEC)
              }
              transactions(last: 1) {
                nodes {
                  id
                  lt
                }
              }
            }
          }
        }
        """
        data = await self.query(q, {"accountId": account_id, "dappId": account_id})
        return data["blockchain"]["account"]

    async def get_indexer_data(self, account_id: str) -> str | None:
        q = """
        query GetIndexerData($accountId: String!, $dappId: String!) {
          blockchain {
            account(account_id: $accountId, dapp_id: $dappId) {
              info { data }
            }
          }
        }
        """
        data = await self.query(q, {"accountId": account_id, "dappId": account_id})
        return data["blockchain"]["account"]["info"]["data"]

    async def get_currency_collection(self) -> dict[str, Any]:
        # Special collection address used by the explorer.
        collection = "8888888888888888888888888888888888888888888888888888888888888888"
        q = """
        query GetCurrencyCollection($accountId: String!, $dappId: String!) {
          blockchain {
            account(account_id: $accountId, dapp_id: $dappId) {
              info {
                data
                code_hash
                init_code_hash
              }
            }
          }
        }
        """
        data = await self.query(q, {"accountId": collection, "dappId": collection})
        return data["blockchain"]["account"]["info"]
