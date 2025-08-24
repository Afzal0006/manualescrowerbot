from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "8350094964:AAHP2RmJ6aCzqthFR9eT6j9-JHAlDOpU6G8"  # tumhara bot token

# Memory
deals = {}

ESCROW_WALLETS = [
    "https://t.me/EscrowWallet1",
    "https://t.me/EscrowWallet2",
    "https://t.me/EscrowWallet3"
]

# /seller command
async def seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    address = " ".join(context.args)

    if not address:
        await update.message.reply_text("❌ Please provide seller address.")
        return

    if chat_id not in deals:
        deals[chat_id] = {"seller": None, "buyer": None, "message_id": None}

    if deals[chat_id]["seller"] is None:
        deals[chat_id]["seller"] = {"id": user.id, "username": user.username, "address": address}
        await update.message.reply_text(
            f"⚡️ SELLER {user.username} UserID: {user.id}\n\n✅ SELLER WALLET\n{address}\n\n"
            f"Now please set the buyer wallet with /buyer <address>"
        )
    else:
        await update.message.reply_text("❌ Seller wallet already set.")

# /buyer command
async def buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    address = " ".join(context.args)

    if not address:
        await update.message.reply_text("❌ Please provide buyer address.")
        return

    if chat_id not in deals:
        deals[chat_id] = {"seller": None, "buyer": None, "message_id": None}

    if deals[chat_id]["buyer"] is None:
        if deals[chat_id].get("seller") and deals[chat_id]["seller"]["address"] == address:
            await update.message.reply_text("❌ Buyer and Seller address is same. Use a different address.")
            return

        deals[chat_id]["buyer"] = {"id": user.id, "username": user.username, "address": address}
        await update.message.reply_text(
            f"⚡️ BUYER {user.username} UserID: {user.id}\n\n✅ BUYER WALLET\n{address}\n\n"
            f"Now you can proceed with /token"
        )
    else:
        await update.message.reply_text("❌ Buyer wallet already set.")

# /token command
async def token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    deal = deals.get(chat_id)

    if not deal or not deal["seller"] or not deal["buyer"]:
        await update.message.reply_text("❌ Set both seller and buyer wallets first.")
        return

    keyboard = [[InlineKeyboardButton("USDT (BEP-20)", callback_data="bep20")]]
    msg = await update.message.reply_text("Select token:", reply_markup=InlineKeyboardMarkup(keyboard))
    deals[chat_id]["message_id"] = msg.message_id

# Handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    user = query.from_user
    deal = deals.get(chat_id)

    if not deal:
        return

    # Step 1: Select Token
    if query.data == "bep20":
        # Save who clicked first
        deal["initiator"] = user.id
        keyboard = [
            [InlineKeyboardButton("✅ Accept", callback_data="accept"),
             InlineKeyboardButton("❌ Reject", callback_data="reject")]
        ]
        await query.message.edit_text(
            "Token selected. Waiting for opponent to Accept/Reject:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Step 2: Accept/Reject
    elif query.data in ["accept", "reject"]:
        initiator = deal.get("initiator")
        opponent = deal["buyer"]["id"] if initiator == deal["seller"]["id"] else deal["seller"]["id"]

        if user.id != opponent:
            await query.answer("❌ Not for you!", show_alert=True)
            return

        if query.data == "reject":
            await query.message.edit_text("❌ Deal Rejected.")
            deals.pop(chat_id, None)
            return

        # Final Deal Created
        escrow = random.choice(ESCROW_WALLETS)
        await query.message.edit_text(
            f"✅ DEAL CREATED\n\n"
            f"⚡️ SELLER WALLET\n{deal['seller']['address']}\n\n"
            f"⚡️ BUYER WALLET\n{deal['buyer']['address']}\n\n"
            f"⚡️ ESCROW WALLET\n[Click Here]({escrow})",
            disable_web_page_preview=True
        )
        deals.pop(chat_id, None)

# Main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("seller", seller))
    app.add_handler(CommandHandler("buyer", buyer))
    app.add_handler(CommandHandler("token", token))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
