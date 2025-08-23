from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8350094964:AAGuq7wGITTob4ASpHj6dxDmVIxppqNlhBY"
USERBOT_CHAT_ID = "7270006608"  # Userbot ka Telegram ID ya username

async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Forward message to userbot
    await context.bot.forward_message(
        chat_id=USERBOT_CHAT_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )
    await update.message.reply_text("Processing your escrow request...")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("Escrow", escrow))
print("Bot running...")
app.run_polling()
