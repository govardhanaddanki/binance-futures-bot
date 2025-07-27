import os
import sys
import logging
from binance.client import Client
from dotenv import load_dotenv
import json

# Load API keys
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Connect to Spot Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# CLI: SYMBOL MIN_PRICE MAX_PRICE NUM_ORDERS QTY
if len(sys.argv) != 6:
    print("Usage: python grid_strategy.py SYMBOL MIN_PRICE MAX_PRICE NUM_ORDERS QTY")
    sys.exit(1)

symbol = sys.argv[1].upper()
min_price = float(sys.argv[2])
max_price = float(sys.argv[3])
num_orders = int(sys.argv[4])
qty = float(sys.argv[5])

if min_price >= max_price or num_orders < 2 or qty <= 0:
    print("❌ Invalid input")
    sys.exit(1)

# Calculate price steps
step = round((max_price - min_price) / (num_orders - 1), 2)
mid_index = num_orders // 2

success_count = 0

print(f"📊 Placing {num_orders} grid orders between {min_price}–{max_price} for {symbol}")

for i in range(num_orders):
    price = round(min_price + step * i, 2)
    side = 'BUY' if i < mid_index else 'SELL'
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=qty,
            price=str(price),
            timeInForce='GTC'
        )
        logging.info(f"✅ Grid {side} Order at {price}: {json.dumps(order)}")
        success_count += 1
    except Exception as e:
        logging.error(f"❌ Failed {side} Order at {price}: {e}")

print(f"✅ Placed {success_count}/{num_orders} grid orders.")
