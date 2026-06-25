from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    text = """
👋 <b>Acki Wallet Bot</b>

Available commands

<code>/wallet &lt;address&gt;</code>

Example

<code>/wallet 0:5ad1c07002dfcaff7a582c7b0765fe7526445d9b4fffe5efe8d5733475f7a5df</code>

The bot will fetch:

🪙 NACKL
🔒 Locked
💵 USDC
🐚 SHELL
⚡ Speed
👆 Total Taps
🎮 MBI Level
"""

    await message.answer(text)
