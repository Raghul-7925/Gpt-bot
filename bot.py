from __future__ import annotations

import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from handlers.start import router as start_router
from handlers.wallet import router as wallet_router
from services.graphql import GraphQLClient
from services.wallet import WalletService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


async def health(request):
    return web.Response(text="OK")


async def start_health_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        int(os.getenv("PORT", "10000")),
    )

    await site.start()
    logger.info("Health server started")


async def main():

    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN not found")

    await start_health_server()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )

    dp = Dispatcher()

    gql = GraphQLClient(settings.graphql_endpoint)
    wallet = WalletService(gql)

    dp["wallet"] = wallet

    dp.include_router(start_router)
    dp.include_router(wallet_router)

    logger.info("Bot started")

    try:
        await dp.start_polling(bot)
    finally:
        await gql.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
