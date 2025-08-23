from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8051082366:AAECqW7-a_x135g2iDpUG7-1_eYowURM7Bw"  # Directly in code

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💫 @Easy_Escrow_Bot 💫
Your Trustworthy Telegram Escrow Service

Welcome to @Easy_Escrow_Bot. This bot provides a reliable escrow service for your transactions on Telegram.
Avoid scams, your funds are safeguarded throughout your deals. If you run into any issues, simply type /dispute and an arbitrator will join the group chat within 24 hours.

🎟 ESCROW FEE:
1.0% Flat

🌐 (UPDATES) - (VOUCHES) ☑️

💬 Proceed with /escrow (to start with a new escrow)

⚠️ IMPORTANT - Make sure coin is same of Buyer and Seller else you may loose your coin.

💡 Type /menu to summon a menu with all bots features")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    app.add_handler(start_handler)
    
    print("Bot is running...")
    app.run_polling()
