import requests
import time
import asyncio
from telegram import Bot

# ===== CONFIG =====
BOT_TOKEN = "8311824260:AAGXb5ZmpaROdX4qdLLyLZYF2QixX_KmKgk"
CHAT_ID = -1002629351743  # Tumhara group chat ID
WALLET_ADDRESS = "0x9a1f5a7f4b78f4A143dBe8271D9393bd60e97365"
API_KEY = "PXMHTYTI6Z5P6ES9M6HFIINZZN41WPKTGD"
POLL_INTERVAL = 15  # seconds

bot = Bot(token=BOT_TOKEN)
last_txn = None

async def monitor_wallet():
    global last_txn
    while True:
        try:
            url = f"https://api.bscscan.com/api?module=account&action=txlist&address={WALLET_ADDRESS}&sort=desc&apikey={API_KEY}"
            r = requests.get(url, timeout=15).json()
            txns = r.get("result", [])
            if txns:
                latest = txns[0]
                if latest["hash"] != last_txn and latest["to"].lower() == WALLET_ADDRESS.lower():
                    last_txn = latest["hash"]
                    value = int(latest["value"]) / 1e18
                    from_addr = latest["from"]
                    tx_hash = latest["hash"]
                    msg = f"✅ New Payment Received!\nAmount: {value:.6f} BNB\nFrom: {from_addr}\nTo: {WALLET_ADDRESS}\n🔗 https://bscscan.com/tx/{tx_hash}"
                    bot.send_message(chat_id=CHAT_ID, text=msg)
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(POLL_INTERVAL)

def main():
    print("🤖 Bot started… monitoring wallet")
    asyncio.run(monitor_wallet())

if __name__ == "__main__":
    main()
