from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import re
import random

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

BEP20_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")

# In-memory storage for the current deal
deal_data = {
    "seller_address": None,
    "seller_user_id": None,
    "buyer_address": None,
    "buyer_user_id": None,
    "token_selected": False,
    "seller_accepted": False,
    "buyer_accepted": False,
    "active": False
}

# /seller command
async def set_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal_data
    user = update.message.from_user
    if deal_data["buyer_user_id"] == user.id:
        await update.message.reply_text("❌ You are already set as buyer. Same ID cannot be seller.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /seller {BEP-20 address}")
        return
    address = context.args[0]
    if not BEP20_PATTERN.match(address):
        await update.message.reply_text("❌ Invalid BEP-20 address!")
        return

    deal_data["seller_address"] = address
    deal_data["seller_user_id"] = user.id
    deal_data["active"] = True
    await update.message.reply_text(
        f"⚡️ SELLER {user.username if user.username else 'No username'} Userid: {user.id}\n\n"
        f"✅ SELLER WALLET\n{address}\n\n"
        "Now please set the buyer wallet with /buyer {address}"
    )

# /buyer command
async def set_buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal_data
    user = update.message.from_user
    if deal_data["seller_user_id"] == user.id:
        await update.message.reply_text("❌ You are already set as seller. Same ID cannot be buyer.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /buyer {BEP-20 address}")
        return
    address = context.args[0]
    if not BEP20_PATTERN.match(address):
        await update.message.reply_text("❌ Invalid BEP-20 address!")
        return
    if deal_data["seller_address"] and address.lower() == deal_data["seller_address"].lower():
        await update.message.reply_text("❌ Buyer and seller address cannot be same.")
        return

    deal_data["buyer_address"] = address
    deal_data["buyer_user_id"] = user.id

    # Send token selection with Accept / Reject
    buttons = [
        [InlineKeyboardButton("Accept", callback_data=f"accept_{user.id}"),
         InlineKeyboardButton("Reject", callback_data=f"reject_{user.id}")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        f"⚡️ BUYER {user.username if user.username else 'No username'} Userid: {user.id}\n\n"
        f"✅ BUYER WALLET\n{address}\n\n"
        "Please confirm the deal by clicking Accept or Reject for USDT BEP-20:",
        reply_markup=keyboard
    )

# Callback for Accept / Reject buttons
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal_data
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if not deal_data["active"]:
        await query.message.reply_text("❌ No active deal.")
        return

    # Accept button
    if data.startswith("accept_"):
        if str(user_id) != data.split("_")[1]:
            await query.message.reply_text("❌ This button is not for you.")
            return
        if user_id == deal_data["seller_user_id"]:
            deal_data["seller_accepted"] = True
        elif user_id == deal_data["buyer_user_id"]:
            deal_data["buyer_accepted"] = True

    # Reject button
    if data.startswith("reject_"):
        if str(user_id) != data.split("_")[1]:
            await query.message.reply_text("❌ This button is not for you.")
            return
        await query.message.reply_text("❌ Deal rejected. Cancelling...")
        deal_data.update({
            "seller_address": None, "seller_user_id": None,
            "buyer_address": None, "buyer_user_id": None,
            "token_selected": False, "seller_accepted": False,
            "buyer_accepted": False, "active": False
        })
        return

    # If both accepted, finalize deal
    if deal_data["seller_accepted"] and deal_data["buyer_accepted"]:
        escrow_address = "0x" + "".join(random.choices("abcdef0123456789", k=40))
        await query.message.reply_text(
            f"✅ Deal Created!\n\n"
            f"Seller address: {deal_data['seller_address']}\n"
            f"Buyer address: {deal_data['buyer_address']}\n"
            f"Escrower address: [Click Here](https://bscscan.com/address/{escrow_address})",
            parse_mode="Markdown"
        )
        # Reset deal
        deal_data.update({
            "seller_address": None, "seller_user_id": None,
            "buyer_address": None, "buyer_user_id": None,
            "token_selected": False, "seller_accepted": False,
            "buyer_accepted": False, "active": False
        })

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("seller", set_seller))
    app.add_handler(CommandHandler("buyer", set_buyer))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is running...")
    app.run_polling()
