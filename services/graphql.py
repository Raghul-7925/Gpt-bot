from __future__ import annotations

import json
from typing import Any

import httpx


class GraphQLClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(20.0),
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "origin": "https://acki.live",
                "referer": "https://acki.live/",
                "user-agent": "Mozilla/5.0 (AckiWalletBot)",
            },
        )

    async def close(self):
        await self.client.aclose()

    async def query(
        self,
        query: str,
        variables: dict[str, Any],
    ) -> dict:

        response = await self.client.post(
            self.endpoint,
            content=json.dumps(
                {
                    "query": query,
                    "variables": variables,
                }
            ),
        )

        response.raise_for_status()

        payload = response.json()

        if payload.get("errors"):
            raise RuntimeError(
                payload["errors"][0]["message"]
            )

        return payload["data"]

    async def get_account(self, address: str):

        query = """
        query GetAccount($accountId:String!, $dappId:String!) {
          blockchain {
            account(
              account_id:$accountId
              dapp_id:$dappId
            ) {
              info {
                balance(format:DEC)

                balance_other {
                  currency
                  value(format:DEC)
                }

                last_paid

                last_trans_lt(format:DEC)

                acc_type

                acc_type_name

                code_hash

                init_code_hash

                data

                boc
              }
            }
          }
        }
        """

        data = await self.query(
            query,
            {
                "accountId": address,
                "dappId": address,
            },
        )

        return data["blockchain"]["account"]["info"]

    async def latest_transaction(
        self,
        address: str,
    ):

        query = """
        query GetLatestTransaction($accountId:String!, $dappId:String!) {
          blockchain {
            account(
              account_id:$accountId
              dapp_id:$dappId
            ) {

              transactions(last:1) {

                nodes {

                  id

                  lt

                  now

                  aborted

                  total_fees(format:DEC)

                }

              }

            }

          }

        }
        """

        data = await self.query(
            query,
            {
                "accountId": address,
                "dappId": address,
            },
        )

        nodes = data["blockchain"]["account"]["transactions"]["nodes"]

        if not nodes:
            return None

        return nodes[0]
