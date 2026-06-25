from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # Telegram
    bot_token: str = os.getenv("BOT_TOKEN", "").strip()

    # Acki Nacki GraphQL
    graphql_endpoint: str = os.getenv(
        "GRAPHQL_ENDPOINT",
        "https://mainnet.ackinacki.org/graphql",
    ).strip()

    # Explorer
    acki_live_endpoint: str = os.getenv(
        "ACKI_LIVE_ENDPOINT",
        "https://acki.live",
    ).strip()

    # Render Port
    port: int = int(os.getenv("PORT", "10000"))

    # Local cache
    aliases_path: Path = Path(
        os.getenv("ALIASES_PATH", "aliases.json")
    )

    # HTTP timeout
    request_timeout: int = int(
        os.getenv("REQUEST_TIMEOUT", "20")
    )

    # Explorer currency mapping
    currency_labels: dict[int, str] = None  # type: ignore

    def __post_init__(self):
        if self.currency_labels is None:
            object.__setattr__(
                self,
                "currency_labels",
                {
                    0: "SHELL",
                    1: "NACKL",
                    2: "LOCKED",
                    3: "USDC",
                    4: "BOOST",
                },
            )


settings = Settings()
