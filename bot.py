from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os

BOT_TOKEN = "8350094964:AAGuq7wGITTob4ASpHj6dxDmVIxppqNlhBY"

async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists("escrow_link.txt"):
        os.remove("escrow_link.txt")

    with open("escrow_request.txt", "w") as f:
        f.write("CREATE_ESCROW")

    await update.message.reply_text("⏳ Escrow group create ho raha hai...")

    for _ in range(20):
        await asyncio.sleep(1)
        if os.path.exists("escrow_link.txt"):
            with open("escrow_link.txt", "r") as f:
                link = f.read().strip()
            await update.message.reply_text(f"✅ Escrow group ready!\n👉 {link}")
            return
    
    await update.message.reply_text("❌ Error: Escrow group banane me problem aayi.")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("escrow", escrow))
app.run_polling()
