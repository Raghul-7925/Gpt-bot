from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.wallet import WalletService

router = Router()


@router.message(Command("wallet"))
async def wallet(
    message: Message,
    wallet: WalletService,
):
    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        await message.answer(
            "Usage:\n<code>/wallet 0:xxxxxxxxxxxxxxxxxxxxxxxx</code>"
        )
        return

    address = parts[1].strip()

    try:
        data = await wallet.get_wallet(address)
    except Exception as e:
        await message.answer(f"❌ {e}")
        return

    await message.answer(
        f"""📊 <b>Wallet Info</b>

📍 <code>{data['address']}</code>

🪙 NACKL: <b>{data['nackl']}</b>

🔒 Locked: <b>{data['locked']}</b>

💵 USDC: <b>{data['usdc']}</b>

🐚 SHELL: <b>{data['shell']}</b>

⚡ Speed: <b>{data['speed']}</b>

👆 Total taps: <b>{data['taps']}</b>

🎮 MBI Level: <b>{data['mbi']}</b>
"""
    )
