# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
from userbot import userbot, create_escrow_group

BOT_TOKEN = "8350094964:AAGuq7wGITTob4ASpHj6dxDmVIxppqNlhBY"

async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ Creating your escrow group...")

        # Userbot start
        await userbot.start()
        link = await create_escrow_group()
        await userbot.stop()

        await update.message.reply_text(f"✅ Escrow group created!\nInvite link: {link}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("escrow", escrow))

print("Bot is running...")
app.run_polling()
