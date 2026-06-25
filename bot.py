\
from aiohttp import web
from health import create_app
import asyncio
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from graphql import GraphQLClient
from handlers.start import router as start_router
from handlers.wallet import router as wallet_router
from wallet import WalletService


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is missing. Put it in your environment or in a .env file.")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    gql = GraphQLClient(settings.graphql_endpoint)
    wallet_service = WalletService(gql)
    bot["wallet_service"] = wallet_service

    dp.include_router(start_router)
    dp.include_router(wallet_router)

    try:
        await dp.start_polling(bot)
    finally:
        await gql.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
