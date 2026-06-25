\
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from wallet import WalletService


router = Router()


def _format_report(report) -> str:
    return (
        "📊 Wallet Info\n\n"
        f"👤 {report.display_name}\n"
        f"🪙 NACKL: {report.nackl}\n"
        f"🔒 Locked: {report.locked}\n"
        f"💵 USDC: {report.usdc}\n"
        f"🐚 SHELL: {report.shell}\n"
        f"⚡ Speed: {report.speed} NACKL/24h\n"
        f"👆 Total taps: {report.total_taps}\n"
        f"🎮 MBI Level: {report.mbi_level}\n\n"
        f"📍 {report.wallet_address}"
    )


@router.message(Command("wallet"))
async def wallet_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer("Usage: /wallet <wallet address>")
        return

    query = args[1].strip()
    service: WalletService = message.bot["wallet_service"]

    try:
        report = await service.get_wallet_report(query)
    except Exception as e:
        await message.answer(f"❌ Could not fetch wallet '{query}': {e}")
        return

    await message.answer(_format_report(report))
