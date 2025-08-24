import requests
import time
from telegram import Bot

BOT_TOKEN = "8311824260:AAGXb5ZmpaROdX4qdLLyLZYF2QixX_KmKgk"
CHAT_ID = "1002776165745"
WALLET_ADDRESS = "0x9a1f5a7f4b78f4A143dBe8271D9393bd60e97365"
API_KEY = "PXMHTYTI6Z5P6ES9M6HFIINZZN41WPKTGD"

bot = Bot(token=BOT_TOKEN)
last_txn = None

def check_transactions():
    global last_txn
    url = f"https://api.bscscan.com/api?module=account&action=txlist&address={WALLET_ADDRESS}&sort=desc&apikey={API_KEY}"
    try:
        r = requests.get(url).json()
        txns = r.get("result", [])
        if not txns:
            return
        latest = txns[0]
        if latest["hash"] != last_txn:
            last_txn = latest["hash"]
            value = int(latest["value"]) / 1e18
            from_addr = latest["from"]
            to_addr = latest["to"]
            msg = f"✅ New Payment Received!\nAmount: {value} BNB\nFrom: {from_addr}\nTo: {to_addr}"
            bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print("Error:", e)

while True:
    check_transactions()
    time.sleep(15)
