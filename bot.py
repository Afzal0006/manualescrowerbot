from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

# Escrow fee
FEE_PERCENT = 1.0  # 1% flat fee

# Messages
WELCOME_MESSAGE = """
I'm normal bot add me grup for deal"""

COMMAND_LIST = """
💻 Available Commands:

/escrow - Start a new escrow
/buyer {deal_id} {crypto_address} - Set buyer address
/seller {deal_id} {crypto_address} - Set seller address
/release {deal_id} - Complete escrow and release funds
/dispute {deal_id} - Start a dispute
/gdeal {deal_id} - View deal status
/menu - Show bot menu
"""

CONTACT_INFO = """
☎️ CONTACT ARBITRATOR

💬 Type /dispute to start a dispute.
💡 Contact @golgibody if no response.
"""

# In-memory storage for deals
active_deals = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Command List", callback_data="show_commands")],
        [InlineKeyboardButton("☎️ CONTACT", callback_data="show_contact")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)

# Menu command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

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
        await start(update, context)

# /escrow command
async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = str(len(active_deals) + 1)
    active_deals[deal_id] = {"buyer": None, "seller": None, "amount": None, "status": "pending"}
    await update.message.reply_text(
        f"🎟 New Escrow Created!\nDeal ID: {deal_id}\n\nUse /buyer {{deal_id}} {{address}} and /seller {{deal_id}} {{address}} to set crypto addresses.\nUse /release {{deal_id}} to complete escrow."
    )

# /buyer command
async def set_buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage: /buyer {deal_id} {crypto_address}")
        return
    deal_id, address = args
    if deal_id not in active_deals:
        await update.message.reply_text("Invalid Deal ID!")
        return
    active_deals[deal_id]["buyer"] = address
    await update.message.reply_text(f"✅ Buyer address for deal {deal_id} set to: {address}")

# /seller command
async def set_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage: /seller {deal_id} {crypto_address}")
        return
    deal_id, address = args
    if deal_id not in active_deals:
        await update.message.reply_text("Invalid Deal ID!")
        return
    active_deals[deal_id]["seller"] = address
    await update.message.reply_text(f"✅ Seller address for deal {deal_id} set to: {address}")

# /release command
async def release(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Usage: /release {deal_id}")
        return
    deal_id = args[0]
    if deal_id not in active_deals:
        await update.message.reply_text("Invalid Deal ID!")
        return
    deal = active_deals[deal_id]
    if not deal["buyer"] or not deal["seller"]:
        await update.message.reply_text("Set both buyer and seller addresses before releasing.")
        return

    # Simulate escrow completion and fee
    amount = 100  # placeholder amount
    fee = (FEE_PERCENT / 100) * amount
    net_amount = amount - fee

    deal["status"] = "completed"
    await update.message.reply_text(
        f"✅ Escrow Completed!\nDeal ID: {deal_id}\nBuyer: {deal['buyer']}\nSeller: {deal['seller']}\nAmount: {amount}\nFee: {fee} ({FEE_PERCENT}%)\nNet Amount: {net_amount}"
    )

# /dispute command
async def dispute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Usage: /dispute {deal_id}")
        return
    deal_id = args[0]
    if deal_id not in active_deals:
        await update.message.reply_text("Invalid Deal ID!")
        return
    await update.message.reply_text(f"⚠️ Dispute started for Deal {deal_id}. An arbitrator will join shortly.")

# /gdeal command
async def view_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Usage: /gdeal {deal_id}")
        return
    deal_id = args[0]
    if deal_id not in active_deals:
        await update.message.reply_text("Invalid Deal ID!")
        return
    deal = active_deals[deal_id]
    await update.message.reply_text(f"Deal {deal_id}:\nBuyer: {deal['buyer']}\nSeller: {deal['seller']}\nStatus: {deal['status']}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("escrow", escrow))
    app.add_handler(CommandHandler("buyer", set_buyer))
    app.add_handler(CommandHandler("seller", set_seller))
    app.add_handler(CommandHandler("release", release))
    app.add_handler(CommandHandler("dispute", dispute))
    app.add_handler(CommandHandler("gdeal", view_deal))

    # Button callback
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is running...")
    app.run_polling()
