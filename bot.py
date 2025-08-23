from pyrogram import Client, filters

# Bot token dalen yahan
BOT_TOKEN = "8350094964:AAGuq7wGITTob4ASpHj6dxDmVIxppqNlhBY"

# Bot ko initialize karen
app = Client("demoescrowerbot", bot_token=BOT_TOKEN)

# /start command handle karne ke liye
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("""
💫 @DemoescrowerBot 💫
Your Trustworthy Telegram Escrow Service

Welcome to @demoescrowerbot This bot provides a reliable escrow service for your transactions on Telegram.
Avoid scams, your funds are safeguarded throughout your deals. If you run into any issues, simply type /dispute and an arbitrator will join the group chat within 24 hours.

🎟 ESCROW FEE:
1.0% Flat

🌐 (UPDATES){Channel link}

💬 Proceed with /escrow (to start with a new escrow)

⚠️ IMPORTANT - Make sure coin is same of Buyer and Seller else you may lose your coin.
""")

# Bot run karein
app.run()
