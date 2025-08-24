from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Your Bot Token
TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

# Store deal data
deals = {}

# Random escrow wallet (static for now)
ESCROW_WALLET = "https://t.me/EscrowWallet1"


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Hey there traders! Welcome to our escrow service.\n\n"
        "⚠️ IMPORTANT - Make sure coin and network is same for Buyer and Seller.\n"
        "⚠️ IMPORTANT - Make sure buyer and seller address are of same chain.\n\n"
        "✅ Please start with /dd to tell deal details."
    )


# /dd command → Ask deal details
async def dd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello there,\nKindly tell deal details i.e.\n\n"
        "Quantity -\nRate -\nConditions (if any) -\n\n"
        "Once filled, set the seller or buyer wallet with /seller or /buyer"
    )


# /seller command
async def seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if len(context.args) != 1:
        await update.message.reply_text("❌ Usage: /seller <wallet_address>")
        return

    wallet = context.args[0]
    deal = deals.setdefault(chat_id, {"seller": None, "buyer": None, "token": None, "message_id": None})

    if deal["seller"]:
        await update.message.reply_text("❌ Seller wallet already set!")
        return

    if deal["buyer"] == wallet:
        await update.message.reply_text("❌ Buyer and Seller address cannot be same!")
        return

    deal["seller"] = {"id": user_id, "username": username, "wallet": wallet}

    text = f"⚡️ SELLER @{username} Userid: {user_id}\n\n✅ SELLER WALLET\n{wallet}\n\nNow please set the buyer wallet with /buyer <address>"
    await update.message.reply_text(text)

    if deal["buyer"]:
        await show_token_option(update, context, deal)


# /buyer command
async def buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if len(context.args) != 1:
        await update.message.reply_text("❌ Usage: /buyer <wallet_address>")
        return

    wallet = context.args[0]
    deal = deals.setdefault(chat_id, {"seller": None, "buyer": None, "token": None, "message_id": None})

    if deal["buyer"]:
        await update.message.reply_text("❌ Buyer wallet already set!")
        return

    if deal["seller"] == wallet:
        await update.message.reply_text("❌ Buyer and Seller address cannot be same!")
        return

    deal["buyer"] = {"id": user_id, "username": username, "wallet": wallet}

    text = f"⚡️ BUYER @{username} Userid: {user_id}\n\n✅ BUYER WALLET\n{wallet}\n\nNow please set the seller wallet with /seller <address>"
    await update.message.reply_text(text)

    if deal["seller"]:
        await show_token_option(update, context, deal)


# Show token selection
async def show_token_option(update: Update, context: ContextTypes.DEFAULT_TYPE, deal):
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("USDT (BEP-20)", callback_data="token_bep20")]]
    msg = await update.message.reply_text("Select token:", reply_markup=InlineKeyboardMarkup(keyboard))
    deal["message_id"] = msg.message_id


# Callback for token selection & accept/reject
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    deal = deals.get(chat_id)

    if not deal:
        await query.answer("❌ No active deal!", show_alert=True)
        return

    # Token selected
    if query.data == "token_bep20":
        # Only first click sets token
        if not deal["token"]:
            deal["token"] = "USDT (BEP-20)"
            keyboard = [
                [InlineKeyboardButton("✅ Accept", callback_data="accept"),
                 InlineKeyboardButton("❌ Reject", callback_data="reject")]
            ]
            await query.edit_message_text(
                f"Token selected: {deal['token']}\nWaiting for opponent to Accept/Reject:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.answer("Token already selected!")

    # Accept/Reject logic
    elif query.data in ["accept", "reject"]:
        if user_id not in [deal["buyer"]["id"], deal["seller"]["id"]]:
            await query.answer("❌ Not for you", show_alert=True)
            return

        opponent_id = deal["buyer"]["id"] if user_id == deal["seller"]["id"] else deal["seller"]["id"]

        if query.data == "reject":
            await query.edit_message_text("❌ Deal Rejected.")
            deals.pop(chat_id, None)
        elif query.data == "accept":
            # Only allow if opponent already accepted
            if deal.get("accepted") == opponent_id:
                await query.edit_message_text(
                    f"✅ DEAL CREATED\n\n"
                    f"⚡️ SELLER WALLET\n{deal['seller']['wallet']}\n\n"
                    f"⚡️ BUYER WALLET\n{deal['buyer']['wallet']}\n\n"
                    f"⚡️ ESCROW WALLET\n{ESCROW_WALLET}"
                )
                deals.pop(chat_id, None)
            else:
                deal["accepted"] = user_id
                await query.answer("✅ You accepted. Waiting for opponent...")


# Run the bot
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dd", dd))
    app.add_handler(CommandHandler("seller", seller))
    app.add_handler(CommandHandler("buyer", buyer))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot is running ✅")   # <--- yaha print add kar diya
    app.run_polling()


if __name__ == "__main__":
    main()
