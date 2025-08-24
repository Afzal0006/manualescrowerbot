import requests
import time
import json
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = "8311824260:AAGXb5ZmpaROdX4qdLLyLZYF2QixX_KmKgk"
WALLET_ADDRESS = "0x9a1f5a7f4b78f4A143dBe8271D9393bd60e97365"
API_KEY = "PXMHTYTI6Z5P6ES9M6HFIINZZN41WPKTGD"
POLL_INTERVAL = 15  # seconds

# ===== STORAGE =====
SUBSCRIBERS_FILE = "subscribers.json"
STATE_FILE = "last_seen.json"

subscribers = set()
state = {"last_tx": ""}

# Load stored data
def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

subscribers = set(load_json(SUBSCRIBERS_FILE, []))
state = load_json(STATE_FILE, {"last_tx": ""})

# ===== BSC SCAN =====
def fetch_latest_tx():
    url = f"https://api.bscscan.com/api?module=account&action=txlist&address={WALLET_ADDRESS}&sort=desc&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=15).json()
        if r.get("status") != "1":
            return None
        txns = r.get("result", [])
        if not isinstance(txns, list) or not txns:
            return None
        return txns[0]
    except:
        return None

# ===== TELEGRAM COMMANDS =====
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Wallet Monitor Bot ready.\nWatching wallet:\n`{WALLET_ADDRESS}`",
        parse_mode="Markdown"
    )

async def watch_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    save_json(SUBSCRIBERS_FILE, list(subscribers))
    await update.message.reply_text("✅ This chat is now subscribed for payment alerts.")

async def unwatch_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        save_json(SUBSCRIBERS_FILE, list(subscribers))
        await update.message.reply_text("🛑 Unsubscribed. No more alerts here.")
    else:
        await update.message.reply_text("ℹ️ This chat was not subscribed.")

# ===== NOTIFY =====
async def notify_all(app, msg):
    for chat_id in subscribers:
        try:
            await app.bot.send_message(chat_id=chat_id, text=msg, disable_web_page_preview=True)
        except:
            continue

def format_tx_message(tx):
    if tx.get("to", "").lower() != WALLET_ADDRESS.lower():
        return ""
    value = int(tx.get("value", "0")) / 1e18
    frm = tx.get("from")
    txh = tx.get("hash")
    msg = f"✅ New Payment Received!\nAmount: {value:.6f} BNB\nFrom: {frm}\nTo: {WALLET_ADDRESS}\n🔗 https://bscscan.com/tx/{txh}"
    return msg

# ===== MONITOR LOOP =====
async def monitor_loop(app):
    global state
    while True:
        tx = fetch_latest_tx()
        if tx:
            txh = tx.get("hash")
            if txh and txh != state.get("last_tx", ""):
                msg = format_tx_message(tx)
                state["last_tx"] = txh
                save_json(STATE_FILE, state)
                if msg:
                    await notify_all(app, msg)
        await asyncio.sleep(POLL_INTERVAL)

# ===== MAIN =====
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("watch", watch_cmd))
    app.add_handler(CommandHandler("unwatch", unwatch_cmd))

    print("🤖 Bot running…")
    # Start background monitor task
    asyncio.create_task(monitor_loop(app))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
