from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("8350094964:AAGuq7wGITTob4ASpHj6dxDmVIxppqNlhBY")  # Heroku environment variable

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hlo I'm ready")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    app.add_handler(start_handler)
    
    print("Bot is running...")
    app.run_polling()
