from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8350094964:AAGuq7wGITTob4ASpHj6dxDmVIxppqNlhBY"
USERBOT_ID = 7270006608   # 👈 apna userbot ka ID yaha daalna

async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user ka command delete
    await update.message.delete()

    # userbot ko /escrow bhejna
    await context.bot.send_message(chat_id=USERBOT_ID, text="/escrow")

    # user ko temporary msg
    await update.effective_chat.send_message("⏳ Escrow group bana raha hu...")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("escrow", escrow))

app.run_polling()
