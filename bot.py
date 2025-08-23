from pyrogram import Client, filters
from pyrogram.types import Message

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

app = Client("demoescrowerbot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    text = """
💫 @DemoescrowerBot 💫
Your Trustworthy Telegram Escrow Service

Welcome to @demoescrowerbot This bot provides a reliable escrow service for your transactions on Telegram.
Avoid scams, your funds are safeguarded throughout your deals. If you run into any issues, simply type /dispute and an arbitrator will join the group chat within 24 hours.

🎟 ESCROW FEE:
1.0% Flat

🌐 (UPDATES){Channel link}

💬 Proceed with /escrow (to start with a new escrow)

⚠️ IMPORTANT - Make sure coin is same of Buyer and Seller else you may lose your coin.
"""
    await message.reply_text(text)

app.run()
