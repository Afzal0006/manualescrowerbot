from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import re

TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

# BEP20 regex
bep20_pattern = re.compile(r"^0x[a-fA-F0-9]{40}$")

# Global deal storage
deal = {
    "buyer": None,
    "buyer_user": None,
    "seller": None,
    "seller_user": None,
    "token": None,
    "status": "pending"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Welcome to Escrow Bot!\n\n"
        "⚠️ IMPORTANT:\n"
        "- Buyer and Seller must use different accounts\n"
        "- Only BEP20 addresses allowed\n\n"
        "✅ Use /buyer <address> and /seller <address> to start"
    )


async def buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal
    user_id = update.effective_user.id

    if deal["buyer"]:
        await update.message.reply_text("❌ Buyer wallet already set!")
        return

    if deal["seller_user"] == user_id:
        await update.message.reply_text("❌ You are already registered as Seller. You cannot be Buyer too!")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /buyer <bep20_address>")
        return

    addr = context.args[0]
    if not bep20_pattern.match(addr):
        await update.message.reply_text("❌ Invalid BEP20 address!")
        return

    if deal["seller"] == addr:
        await update.message.reply_text("❌ Buyer and Seller address cannot be same!")
        return

    deal["buyer"] = addr
    deal["buyer_user"] = user_id

    await update.message.reply_text(
        f"⚡️ BUYER {update.effective_user.username} Userid: {user_id}\n\n"
        f"✅ BUYER WALLET\n{addr}"
    )

    # Agar dono set ho gaye to token option dikhao
    if deal["seller"]:
        await show_token_option(update, context)


async def seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal
    user_id = update.effective_user.id

    if deal["seller"]:
        await update.message.reply_text("❌ Seller wallet already set!")
        return

    if deal["buyer_user"] == user_id:
        await update.message.reply_text("❌ You are already registered as Buyer. You cannot be Seller too!")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /seller <bep20_address>")
        return

    addr = context.args[0]
    if not bep20_pattern.match(addr):
        await update.message.reply_text("❌ Invalid BEP20 address!")
        return

    if deal["buyer"] == addr:
        await update.message.reply_text("❌ Buyer and Seller address cannot be same!")
        return

    deal["seller"] = addr
    deal["seller_user"] = user_id

    await update.message.reply_text(
        f"⚡️ SELLER {update.effective_user.username} Userid: {user_id}\n\n"
        f"✅ SELLER WALLET\n{addr}"
    )

    # Agar dono set ho gaye to token option dikhao
    if deal["buyer"]:
        await show_token_option(update, context)


async def show_token_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 USDT (BEP20)", callback_data="token_bep20")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✅ Both Buyer and Seller wallets are set!\n\n"
        "👉 Please choose a token for the deal:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deal
    query = update.callback_query
    await query.answer()

    if query.data == "token_bep20":
        deal["token"] = "USDT BEP20"
        keyboard = [
            [InlineKeyboardButton("✅ Accept", callback_data="accept"),
             InlineKeyboardButton("❌ Reject", callback_data="reject")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"💠 Token selected: {deal['token']}\n\n"
            f"⚡ Seller: {deal['seller']}\n"
            f"⚡ Buyer: {deal['buyer']}\n\n"
            f"👉 Now click Accept/Reject:",
            reply_markup=reply_markup
        )

    elif query.data == "accept":
        deal["status"] = "accepted"
        await query.edit_message_text("✅ Deal Accepted! Funds can now be transferred to Escrow Wallet.")

    elif query.data == "reject":
        deal["status"] = "rejected"
        await query.edit_message_text("❌ Deal Rejected!")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buyer", buyer))
    app.add_handler(CommandHandler("seller", seller))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
