# Acki Wallet Bot

A simple Telegram bot that fetches wallet data from Acki Nacki GraphQL.

## Features
- `/start`
- `/help`
- `/wallet <address>`
- `/wallet <name>` for names listed in `aliases.json`

## Setup
1. Create a Telegram bot with @BotFather.
2. Put the token into `.env`:
   ```env
   BOT_TOKEN=123456:ABC...
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python bot.py
   ```

## Notes
- This is a read-only first version.
- `aliases.json` can be extended to map names to wallet addresses.
- Currency labels and contract-specific decoding can be extended in `decoder.py`.
