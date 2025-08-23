from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ChatMemberHandler

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

# Messages
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

GROUP_WELCOME = """
📍 Hey there traders! Welcome to our escrow service.
⚠️ IMPORTANT - Make sure coin and network is same of Buyer and Seller else you may lose your coin.
⚠️ IMPORTANT - Make sure the /buyer address and /seller address are of same chain else you may lose your coin.

✅ Please start with /dd command and if you have any doubts please use /start command.
"""

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Command List", callback_data="show_commands")],
        [InlineKeyboardButton("☎️ CONTACT", callback_data="show_contact")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)

# Button callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_commands":
        buttons = [[InlineKeyboardButton("Back", callback_data="show_start")]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(COMMAND_LIST, reply_markup=keyboard)

    elif query.data == "show_contact":
        buttons = [[InlineKeyboardButton("Back", callback_data="show_start")]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(CONTACT_INFO, reply_markup=keyboard)

    elif query.data == "show_start":
        buttons = [
            [InlineKeyboardButton("Command List", callback_data="show_commands")],
            [InlineKeyboardButton("☎️ CONTACT", callback_data="show_contact")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(WELCOME_MESSAGE, reply_markup=keyboard)

# Detect when bot is added to a group
async def added_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.chat_member.chat
    new_status = update.chat_member.new_chat_member.status
    old_status = update.chat_member.old_chat_member.status

    # If bot was added to a group (member status changed to 'member' or 'administrator')
    if new_status in ["member", "administrator"] and old_status in ["left", "kicked"]:
        await context.bot.send_message(chat_id=chat.id, text=GROUP_WELCOME)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(ChatMemberHandler(added_to_group, ChatMemberHandler.MY_CHAT_MEMBER))

    print("Bot is running...")
    app.run_polling()
