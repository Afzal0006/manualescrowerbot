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

💡 Tap buttons below to see available commands or contact info.
"""

COMMAND_LIST = """
💻 Available Commands:

/seller {crypto address} - Set seller crypto address
/buyer {crypto address} - Set buyer crypto address
/dispute - Start a dispute
/escrow - Start a new escrow
/menu - Show bot menu
"""

CONTACT_INFO = """
☎️ CONTACT ARBITRATOR

💬 Type /dispute

💡 In case you're not getting a response, you can reach out to @golgibody
"""

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Command List", callback_data="show_commands")],
        [InlineKeyboardButton("☎️ CONTACT", callback_data="show_contact")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)

# Callback for button tap
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_commands":
        # Show command list with Back button
        buttons = [
            [InlineKeyboardButton("Back", callback_data="show_start")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(COMMAND_LIST, reply_markup=keyboard)

    elif query.data == "show_contact":
        # Show contact info with Back button
        buttons = [
            [InlineKeyboardButton("Back", callback_data="show_start")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(CONTACT_INFO, reply_markup=keyboard)

    elif query.data == "show_start":
        # Go back to start message with main buttons
        buttons = [
            [InlineKeyboardButton("Command List", callback_data="show_commands")],
            [InlineKeyboardButton("☎️ CONTACT", callback_data="show_contact")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(WELCOME_MESSAGE, reply_markup=keyboard)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot is running...")
    app.run_polling()
