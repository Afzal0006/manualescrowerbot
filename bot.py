from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import re

TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"

# Deal storage
deal = {
    "seller": None, "buyer": None,
    "seller_user": None, "buyer_user": None,
    "msg_id": None, "chat_id": None,
    "token": None, "accepted": False
}

# Regex for BEP20 address validation
bep20_pattern = re.compile(r"^0x[a-fA-F0-9]{40}$")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Welcome! Use /seller or /buyer to set wallet address.")

async def seller(update: Update, context: CallbackContext):
    global deal
    user_id = update.effective_user.id

    if deal["seller"]:
        await update.message.reply_text("❌ Seller wallet already set!")
        return

    # Prevent same person from being both seller and buyer
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
        f"✅ SELLER WALLET\n{addr}\n\nNow please set the buyer wallet with /buyer <address>"
    )

    if deal["buyer"]:
        await show_token_option(update, context)

async def buyer(update: Update, context: CallbackContext):
    global deal
    user_id = update.effective_user.id

    if deal["buyer"]:
        await update.message.reply_text("❌ Buyer wallet already set!")
        return

    # Prevent same person from being both buyer and seller
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
        f"✅ BUYER WALLET\n{addr}\n\nNow please set the seller wallet with /seller <address>"
    )

    if deal["seller"]:
        await show_token_option(update, context)

async def show_token_option(update: Update, context: CallbackContext):
    global deal
    keyboard = [[InlineKeyboardButton("USDT BEP20", callback_data="token_bep20")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = await update.message.reply_text("💠 Select token:", reply_markup=reply_markup)
    deal["msg_id"] = msg.message_id
    deal["chat_id"] = msg.chat.id

async def button_handler(update: Update, context: CallbackContext):
    global deal
    query = update.callback_query
    await query.answer()

    # Token Selection
    if query.data == "token_bep20":
        deal["token"] = "USDT BEP20"
        keyboard = [
            [InlineKeyboardButton("✅ Accept", callback_data="accept"),
             InlineKeyboardButton("❌ Reject", callback_data="reject")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"💠 Token selected: {deal['token']}\nWaiting for opponent to Accept/Reject:",
            reply_markup=reply_markup
        )

    # Accept/Reject
    elif query.data in ["accept", "reject"]:
        user_id = query.from_user.id

        # Ensure only buyer or seller can click
        if user_id not in [deal["buyer_user"], deal["seller_user"]]:
            await query.answer("⚠️ Only Buyer or Seller can respond!", show_alert=True)
            return

        if query.data == "reject":
            await query.edit_message_text("❌ Deal Rejected!")
            reset_deal()
            return

        if not deal["accepted"]:
            deal["accepted"] = user_id
            await query.edit_message_text("✅ One side accepted. Waiting for the opponent...")
        else:
            # Ensure second accept comes from the other user
            if deal["accepted"] == user_id:
                await query.answer("⚠️ You already accepted! Waiting for the opponent.", show_alert=True)
                return

            escrow = "https://t.me/EscrowWalletDemo"
            await query.edit_message_text(
                f"✅ DEAL CREATED\n\n"
                f"⚡️ SELLER WALLET\n{deal['seller']}\n\n"
                f"⚡️ BUYER WALLET\n{deal['buyer']}\n\n"
                f"⚡️ ESCROW WALLET\n<a href='{escrow}'>Click Here</a>",
                parse_mode="HTML"
            )
            reset_deal()

def reset_deal():
    global deal
    deal = {
        "seller": None, "buyer": None,
        "seller_user": None, "buyer_user": None,
        "msg_id": None, "chat_id": None,
        "token": None, "accepted": False
    }

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("seller", seller))
    app.add_handler(CommandHandler("buyer", buyer))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
