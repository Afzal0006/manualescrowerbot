from pyrogram import Client, filters

# Sirf BOT_TOKEN chahiye, api_id/hash ki zarurat nahi
BOT_TOKEN = "8350094964:AAGuq7wGITTob4ASpHj6dxDmVIxppqNlhBY"

# Initialize bot
app = Client(
    "demoescrowerbot",
    bot_token=BOT_TOKEN
)

# /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "💫 @DemoescrowerBot 💫\n"
        "Your Trustworthy Telegram Escrow Service\n\n"
        "Welcome to @demoescrowerbot. This bot provides a reliable escrow service for your transactions on Telegram.\n"
        "Avoid scams, your funds are safeguarded throughout your deals. If you run into any issues, type /dispute and an arbitrator will join the group chat within 24 hours.\n\n"
        "🎟 ESCROW FEE:\n1.0% Flat\n\n"
        "🌐 (UPDATES){Channel link}\n\n"
        "💬 Proceed with /escrow (to start with a new escrow)\n\n"
        "⚠️ IMPORTANT - Make sure coin is same of Buyer and Seller else you may lose your coin."
    )

# Run bot
app.run()
