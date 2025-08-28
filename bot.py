import requests
import time
from telegram import Bot

# ===== CONFIG =====
BSC_API_KEY = "EF7ZUA5EZKWDTEJSH525RNRCSDQQ1TVS6P"  # Aapki BscScan API key
WALLET_ADDRESS = "0xfcfdcad750dcb37211ec494a0a625dba3e99b4d5"  # Aapka BEP-20 wallet address
TOKEN_CONTRACT = ""  # Agar specific token track karna ho to contract address yahan, warna leave blank
TELEGRAM_BOT_TOKEN = "8466069044:AAGchh9WGQZh1fYUQkLdNpFgKsM5IT6mgEc"  # Telegram bot token
TELEGRAM_CHAT_ID = -1002591009357  # Telegram group chat ID
CHECK_INTERVAL = 15  # seconds

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Store already notified transactions
notified_txs = set()

def get_bep20_transactions(wallet):
    url = f"https://api.bscscan.com/api?module=account&action=tokentx&address={wallet}&startblock=0&endblock=99999999&sort=desc&apikey={BSC_API_KEY}"
    response = requests.get(url).json()
    if response["status"] == "1":
        return response["result"]
    return []

print("✅ Bot is running...")   # <-- Ye message startup pe print hoga

while True:
    try:
        transactions = get_bep20_transactions(WALLET_ADDRESS)
        if transactions:
            for tx in transactions:
                tx_hash = tx["hash"]
                # Optional: filter by token contract
                if TOKEN_CONTRACT and tx["contractAddress"].lower() != TOKEN_CONTRACT.lower():
                    continue
                if tx_hash not in notified_txs:
                    notified_txs.add(tx_hash)
                    amount = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
                    message = (
                        f"💰 New Transaction Detected!\n"
                        f"From: {tx['from']}\n"
                        f"To: {tx['to']}\n"
                        f"Token: {tx['tokenName']} ({tx['tokenSymbol']})\n"
                        f"Amount: {amount}\n"
                        f"Tx Hash: https://bscscan.com/tx/{tx_hash}"
                    )
                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print("Error:", e)
        time.sleep(CHECK_INTERVAL)
