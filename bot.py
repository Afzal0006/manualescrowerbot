from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

WELCOME_MESSAGE = """
💫 @Easy_Escrow_Bot 💫
Your Trustworthy Telegram Escrow Service

Welcome to @Easy_Escrow_Bot. This bot provides a reliable escrow service for your transactions on Telegram.
Avoid scams, your funds are safeguarded throughout your deals. If you run into any issues, simply type /dispute and an arbitrator will join the group chat within 24 hours.

🎟 ESCROW FEE:
1.0% Flat

💬 Proceed with /escrow (to start with a new escrow)

⚠️ IMPORTANT - Make sure coin is same of Buyer and Seller else you may lose your coin.

💡 Tap "Command List" button below to see available commands.
"""

# Command list text
COMMAND_LIST = """
💻 Available Commands:

/seller {crypto address} - Set seller crypto address
/buyer {crypto address} - Set buyer crypto address
/dispute - Start a dispute
/escrow - Start a new escrow
/menu - Show bot menu
"""

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create a button that shows commands
    buttons = [
        [InlineKeyboardButton("Command List", callback_data="show_commands")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)

# Callback for button tap
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    if query.data == "show_commands":
        await query.message.reply_text(COMMAND_LIST)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot is running...")
    app.run_polling()
