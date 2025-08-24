from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import re
import random

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

BEP20_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")

# In-memory storage
deal_data = {
    "seller_address": None,
    "buyer_address": None,
    "seller_user": None,
    "buyer_user": None,
    "token_selected": False,
    "token_confirmed": False,
}

# /seller command
async def set_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal_data
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /seller {BEP-20 address}")
        return
    address = context.args[0]
    if not BEP20_PATTERN.match(address):
        await update.message.reply_text("❌ Invalid BEP-20 address! It must start with 0x and be 42 characters long.")
        return
    deal_data["seller_address"] = address
    user = update.message.from_user
    deal_data["seller_user"] = user
    await update.message.reply_text(
        f"⚡️ SELLER {user.username if user.username else 'No username'} Userid: {user.id}\n\n"
        f"✅ SELLER WALLET\n{address}\n\n"
        "Now please set the buyer wallet with /buyer {address}"
    )

# /buyer command
async def set_buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal_data
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /buyer {BEP-20 address}")
        return
    address = context.args[0]
    if not BEP20_PATTERN.match(address):
        await update.message.reply_text("❌ Invalid BEP-20 address! It must start with 0x and be 42 characters long.")
        return
    if deal_data["seller_address"] and address.lower() == deal_data["seller_address"].lower():
        await update.message.reply_text("❌ Buyer and seller address is same. Please use a different address.")
        return
    deal_data["buyer_address"] = address
    user = update.message.from_user
    deal_data["buyer_user"] = user

    # Send token selection button
    buttons = [[InlineKeyboardButton("USDT BEP-20", callback_data="token_usdt")]]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        f"⚡️ BUYER {user.username if user.username else 'No username'} Userid: {user.id}\n\n"
        f"✅ BUYER WALLET\n{address}\n\n"
        "Please select token to proceed:",
        reply_markup=keyboard
    )

# Button callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal_data
    query = update.callback_query
    await query.answer()
    
    if query.data == "token_usdt":
        if not deal_data["token_selected"]:
            deal_data["token_selected"] = True
            await query.message.reply_text(
                "Token selected: USDT BEP-20\nWaiting for the other party to accept..."
            )
        else:
            deal_data["token_confirmed"] = True

    # Check if both confirmed
    if deal_data["token_selected"] and deal_data["token_confirmed"]:
        # Random escrower address
        escrow_address = "0x" + "".join(random.choices("abcdef0123456789", k=40))
        seller_addr = deal_data["seller_address"]
        buyer_addr = deal_data["buyer_address"]
        await query.message.reply_text(
            f"✅ Deal Created!\n\n"
            f"Seller address: {seller_addr}\n"
            f"Buyer address: {buyer_addr}\n"
            f"Escrower address: [Click Here](https://bscscan.com/address/{escrow_address})",
            parse_mode="Markdown"
        )
        # Reset deal
        deal_data.update({
            "seller_address": None,
            "buyer_address": None,
            "seller_user": None,
            "buyer_user": None,
            "token_selected": False,
            "token_confirmed": False,
        })

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("seller", set_seller))
    app.add_handler(CommandHandler("buyer", set_buyer))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is running...")
    app.run_polling()
