from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

WELCOME_MESSAGE = "I'm normal bot add me grup for deal"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inline button to add bot in a group
    buttons = [
        [InlineKeyboardButton("➕ Add me in Group", url="https://t.me/Eueue8w98bot?startgroup=true")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handler
    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()
