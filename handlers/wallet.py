from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.wallet import WalletService

router = Router()


@router.message(Command("wallet"))
async def wallet(message: Message):

    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        await message.answer(
            "Usage:\n<code>/wallet 0:address</code>"
        )
        return

    address = parts[1].strip()

    # Get WalletService from Dispatcher
    wallet_service: WalletService = message.dispatcher["wallet"]

    try:
        data = await wallet_service.get_wallet(address)

    except Exception as e:
        await message.answer(
            f"❌ Error\n\n<code>{e}</code>"
        )
        return

    text = f"""
📊 <b>Wallet Info</b>

📍 <code>{data['address']}</code>

🪙 NACKL: <b>{data['nackl']}</b>

🔒 Locked: <b>{data['locked']}</b>

💵 USDC: <b>{data['usdc']}</b>

🐚 SHELL: <b>{data['shell']}</b>

⚡ Speed: <b>{data['speed'] or 'Unknown'}</b>

👆 Total taps: <b>{data['taps'] or 'Unknown'}</b>

🎮 MBI Level: <b>{data['mbi'] or 'Unknown'}</b>
"""

    await message.answer(text)
