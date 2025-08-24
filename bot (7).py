import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

BOT_TOKEN = "8350094964:AAE-ebwWQBx_YWnW_stEqcxiKKVVx8SZaAw"

START_MESSAGE = (
    "Direct P#rn Video Channel 🌸\n\n"
    "D#si Maal Ke Deewano Ke Liye 😋\n\n"
    "No Sn#ps Pure D#si Maal 😙\n\n"
    "51000+ rare D#si le#ks ever.... 🎀\n\n"
    "Just pay and get entry...\n\n"
    "Direct video No Link - Ads Sh#t 🔥\n\n"
    "Price :- ₹69/-\n\n"
    "Validity :- lifetime"
)

PREMIUM_MESSAGE = "Hlo dm for premium @golgibody"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")],
        [InlineKeyboardButton("🎥 Premium Demo", url="https://t.me/SexyEmoji")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.delete()
    await update.message.reply_text(START_MESSAGE, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "get_premium":
        keyboard = [
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
            [InlineKeyboardButton("🎥 Premium Demo", url="https://t.me/SexyEmoji")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(PREMIUM_MESSAGE, reply_markup=reply_markup)
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")],
            [InlineKeyboardButton("🎥 Premium Demo", url="https://t.me/SexyEmoji")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(START_MESSAGE, reply_markup=reply_markup)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot started successfully ✅")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    asyncio.run(main())
