from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

WELCOME_MESSAGE = "I'm normal bot add me grup for deal"

# Regex pattern for BEP-20 address (starts with 0x and 40 hex chars)
BEP20_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")

# In-memory storage for addresses
buyer_address = None
seller_address = None

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("➕ Add me in Group", url="https://t.me/Eueue8w98bot?startgroup=true")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)

# /buyer command
async def set_buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global buyer_address, seller_address
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /buyer {BEP-20 address}")
        return
    address = context.args[0]
    if not BEP20_PATTERN.match(address):
        await update.message.reply_text("❌ Invalid BEP-20 address! It must start with 0x and be 42 characters long.")
        return
    if seller_address and address.lower() == seller_address.lower():
        await update.message.reply_text("❌ Buyer and seller address is same. Please use a different address.")
        return
    buyer_address = address
    await update.message.reply_text(f"✅ Buyer address set: {address}")

# /seller command
async def set_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global buyer_address, seller_address
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /seller {BEP-20 address}")
        return
    address = context.args[0]
    if not BEP20_PATTERN.match(address):
        await update.message.reply_text("❌ Invalid BEP-20 address! It must start with 0x and be 42 characters long.")
        return
    if buyer_address and address.lower() == buyer_address.lower():
        await update.message.reply_text("❌ Buyer and seller address is same. Please use a different address.")
        return
    seller_address = address
    await update.message.reply_text(f"✅ Seller address set: {address}")

# /dd command - Deal details template
async def deal_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Hello there,\n"
        "Kindly tell deal details i.e.\n\n"
        "Quantity -\n"
        "Rate -\n"
        "Conditions (if any) -\n\n"
        "Remember without it disputes wouldn’t be resolved. Once filled, proceed with "
        "Specifications of the seller or buyer with /seller or /buyer [CRYPTO ADDRESS]"
    )
    await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buyer", set_buyer))
    app.add_handler(CommandHandler("seller", set_seller))
    app.add_handler(CommandHandler("dd", deal_details))  # /dd is now the deal template

    print("Bot is running...")
    app.run_polling()
