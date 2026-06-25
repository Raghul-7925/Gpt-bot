from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "").strip()
    graphql_endpoint: str = os.getenv(
        "GRAPHQL_ENDPOINT",
        "https://mainnet.ackinacki.org/graphql",
    ).strip()
    acki_live_endpoint: str = os.getenv(
        "ACKI_LIVE_ENDPOINT",
        "https://acki.live",
    ).strip()
    aliases_path: Path = Path(os.getenv("ALIASES_PATH", "aliases.json"))

    currency_labels: dict[int, str] = None  # type: ignore

    def __post_init__(self):
        if self.currency_labels is None:
            object.__setattr__(
                self,
                "currency_labels",
                {
                    0: "SHELL",
                    1: "NACKL",
                    2: "Locked",
                    3: "USDC",
                    4: "BOOST",
                },
            )


settings = Settings()
