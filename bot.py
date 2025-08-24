from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import re

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"
ESCROW_WALLET = "0xEscrowWalletExample1234567890abcdef12345678"

# Deal storage
deal = {"seller": None, "buyer": None, "seller_id": None, "buyer_id": None,
        "seller_username": None, "buyer_username": None, "status": None}


# Validate wallet address
def valid_wallet(address: str) -> bool:
    return bool(re.fullmatch(r"0x[a-fA-F0-9]{40}", address))


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 Welcome to Escrow Bot!\nUse /seller or /buyer to set wallets.")


# /seller command
async def seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"

    if deal["seller"]:
        await update.message.reply_text("❌ Seller wallet already set.")
        return
    if deal["buyer_id"] == user_id:
        await update.message.reply_text("❌ You cannot be both Buyer and Seller.")
        return
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /seller <wallet_address>")
        return

    wallet = context.args[0]
    if not valid_wallet(wallet):
        await update.message.reply_text("❌ Invalid wallet address! Must be a valid BEP20 (starts with 0x...).")
        return

    deal.update({"seller": wallet, "seller_id": user_id, "seller_username": username})
    await update.message.reply_text(f"⚡ SELLER {username} (ID: {user_id})\n\n💳 Seller Wallet:\n{wallet}")

    if deal["buyer"]:
        await token_ready(update, context)


# /buyer command
async def buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"

    if deal["buyer"]:
        await update.message.reply_text("❌ Buyer wallet already set.")
        return
    if deal["seller_id"] == user_id:
        await update.message.reply_text("❌ You cannot be both Buyer and Seller.")
        return
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /buyer <wallet_address>")
        return

    wallet = context.args[0]
    if not valid_wallet(wallet):
        await update.message.reply_text("❌ Invalid wallet address! Must be a valid BEP20 (starts with 0x...).")
        return

    deal.update({"buyer": wallet, "buyer_id": user_id, "buyer_username": username})
    await update.message.reply_text(f"⚡ BUYER {username} (ID: {user_id})\n\n💳 Buyer Wallet:\n{wallet}")

    if deal["seller"]:
        await token_ready(update, context)


# Show /token option
async def token_ready(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("USDT (BEP20)", callback_data="token_bep20")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✅ Both wallets set!\nNow select a token:", reply_markup=reply_markup)


# Handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "token_bep20":
        deal["initiator"] = user_id
        keyboard = [
            [InlineKeyboardButton("✅ Accept", callback_data="accept")],
            [InlineKeyboardButton("❌ Reject", callback_data="reject")]
        ]
        await query.edit_message_text("💠 Token selected: USDT (BEP20)\n\nWaiting for opponent to Accept/Reject:",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "accept":
        if user_id == deal.get("initiator"):
            await query.answer("❌ Not for you!", show_alert=True)
            return
        deal["status"] = "accepted"
        await query.edit_message_text(
            f"✅ DEAL ACCEPTED!\n\n"
            f"⚡ SELLER: @{deal['seller_username']} (ID: {deal['seller_id']})\n"
            f"💳 Seller Wallet:\n{deal['seller']}\n\n"
            f"⚡ BUYER: @{deal['buyer_username']} (ID: {deal['buyer_id']})\n"
            f"💳 Buyer Wallet:\n{deal['buyer']}\n\n"
            f"🔒 Escrow Wallet: [Click Here](https://bscscan.com/address/{ESCROW_WALLET})",
            parse_mode="Markdown"
        )

    elif query.data == "reject":
        if user_id == deal.get("initiator"):
            await query.answer("❌ Not for you!", show_alert=True)
            return
        deal["status"] = "rejected"
        await query.edit_message_text("❌ Deal Rejected!")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("seller", seller))
    app.add_handler(CommandHandler("buyer", buyer))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
