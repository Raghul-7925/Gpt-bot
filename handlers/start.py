\
from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart, Command

from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Send /wallet <address> to fetch wallet stats.\n\n"
        "Example:\n"
        "/wallet 0:8c478bedb9ffdb890f1e82de78d5edbb0f2af2d4162952a41a99ab9c22871ae7"
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Commands:\n"
        "/start\n"
        "/help\n"
        "/wallet <wallet address>\n\n"
        "Note: name resolution is a later enhancement."
    )
