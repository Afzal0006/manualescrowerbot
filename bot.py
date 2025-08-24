from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import re
import random

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"
BEP20_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")

# Deal storage
deal_data = {
    "seller_address": None,
    "seller_user_id": None,
    "buyer_address": None,
    "buyer_user_id": None,
    "token_selected_by": None,
    "opponent_accepted": False,
    "active": False
}

# /seller command
async def set_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Prevent resetting once set
    if deal_data["seller_address"] is not None:
        await update.message.reply_text("❌ Seller already set, cannot change again.")
        return

    if deal_data["buyer_user_id"] == user.id:
        await update.message.reply_text("❌ Same ID cannot be both buyer and seller.")
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

    await update.message.reply_text(f"⚡️ SELLER WALLET\n{address}")

    # Check if both set
    if deal_data["buyer_address"] and deal_data["seller_address"]:
        await update.message.reply_text("✅ Both addresses set! Use /token to continue.")

# /buyer command
async def set_buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Prevent resetting once set
    if deal_data["buyer_address"] is not None:
        await update.message.reply_text("❌ Buyer already set, cannot change again.")
        return

    if deal_data["seller_user_id"] == user.id:
        await update.message.reply_text("❌ Same ID cannot be both seller and buyer.")
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
    deal_data["active"] = True

    await update.message.reply_text(f"⚡️ BUYER WALLET\n{address}")

    # Check if both set
    if deal_data["buyer_address"] and deal_data["seller_address"]:
        await update.message.reply_text("✅ Both addresses set! Use /token to continue.")

# /token command
async def token_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not deal_data["buyer_address"] or not deal_data["seller_address"]:
        await update.message.reply_text("❌ Both addresses must be set first.")
        return

    buttons = [[InlineKeyboardButton("BEP-20", callback_data=f"bep20_{update.effective_user.id}")]]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Select token:", reply_markup=keyboard)

# Callback for buttons
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if not deal_data["active"]:
        await query.message.reply_text("❌ No active deal.")
        return

    # Check if button is for this user
    if data.startswith("bep20_"):
        target_id = int(data.split("_")[1])
        if user_id != target_id:
            await query.message.reply_text("❌ Not for you!")
            return
        deal_data["token_selected_by"] = user_id
        # Send Accept/Reject to opponent
        opponent_id = deal_data["seller_user_id"] if user_id == deal_data["buyer_user_id"] else deal_data["buyer_user_id"]
        buttons = [[InlineKeyboardButton("Accept", callback_data=f"accept_{opponent_id}"),
                    InlineKeyboardButton("Reject", callback_data=f"reject_{opponent_id}")]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.reply_text("Token selected. Waiting for opponent to Accept/Reject:", reply_markup=keyboard)
        return

    # Handle Accept / Reject
    if data.startswith("accept_") or data.startswith("reject_"):
        target_id = int(data.split("_")[1])
        if user_id != target_id:
            await query.message.reply_text("❌ Not for you!")
            return
        if data.startswith("reject_"):
            await query.message.reply_text("❌ Deal rejected. Cancelling...")
            for k in deal_data.keys():
                deal_data[k] = None
            return
        # Accept -> finalize deal
        escrow_address = "0x" + "".join(random.choices("abcdef0123456789", k=40))
        await query.message.reply_text(
            f"✅ DEAL CREATED\n\n"
            f"⚡️ SELLER WALLET\n{deal_data['seller_address']}\n\n"
            f"⚡️ BUYER WALLET\n{deal_data['buyer_address']}\n\n"
            f"⚡️ ESCROW WALLET\n[Click Here](https://bscscan.com/address/{escrow_address})",
            parse_mode="Markdown"
        )
        # Reset deal
        for k in deal_data.keys():
            deal_data[k] = None

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("seller", set_seller))
    app.add_handler(CommandHandler("buyer", set_buyer))
    app.add_handler(CommandHandler("token", token_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot running...")
    app.run_polling()
