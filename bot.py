from __future__ import annotations

import os
import logging
import asyncio

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from graphql import GraphQLClient
from handlers.start import router as start_router
from handlers.wallet import router as wallet_router
from wallet import WalletService
from health import create_app


logging.basicConfig(level=logging.INFO)


async def start_health_server():
    app = create_app()

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        int(os.getenv("PORT", "10000")),
    )

    await site.start()
    logging.info("Health server started.")


async def main() -> None:
    if not settings.bot_token:
        raise RuntimeError(
            "BOT_TOKEN is missing. Set it in Render Environment Variables."
        )

    # Start HTTP server (needed for Render Web Service)
    await start_health_server()

    # Telegram Bot
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    # GraphQL
    gql = GraphQLClient(settings.graphql_endpoint)
    wallet_service = WalletService(gql)

    bot["wallet_service"] = wallet_service

    # Routers
    dp.include_router(start_router)
    dp.include_router(wallet_router)

    logging.info("Bot started successfully.")

    try:
        await dp.start_polling(bot)
    finally:
        logging.info("Stopping bot...")

        await gql.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
