import os
import sys
import logging
from binance.client import Client
from dotenv import load_dotenv
import json
import time

# Load .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Binance Spot Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Args: SYMBOL SIDE TOTAL_QTY SPLIT_COUNT INTERVAL
if len(sys.argv) != 6:
    print("Usage: python twap.py SYMBOL SIDE TOTAL_QTY SPLIT_COUNT INTERVAL_SEC")
    sys.exit(1)

symbol = sys.argv[1].upper()
side = sys.argv[2].upper()
total_qty = float(sys.argv[3])
split_count = int(sys.argv[4])
interval = int(sys.argv[5])

# Validation
if side not in ['BUY', 'SELL'] or total_qty <= 0 or split_count <= 0 or interval < 0:
    print("❌ Invalid input")
    sys.exit(1)

chunk_qty = round(total_qty / split_count, 6)

success_count = 0
for i in range(split_count):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=chunk_qty
        )
        logging.info("✅ TWAP Order %d Placed: %s", i+1, json.dumps(order))
        success_count += 1
    except Exception as e:
        logging.error(f"❌ TWAP Order {i+1} Failed: {e}")

    if i < split_count - 1:
        time.sleep(interval)

# ✅ Final Single-Line Output
print(f"✅ Placed {success_count}/{split_count} TWAP market orders ({chunk_qty} {symbol} each)")
