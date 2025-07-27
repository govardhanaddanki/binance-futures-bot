import json  # ⬅️ Add this at the top with other imports
import os
import sys
import logging
from binance.client import Client
from dotenv import load_dotenv

# Load API credentials
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Setup logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Connect to Spot Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Validate CLI arguments
if len(sys.argv) != 6:
    print("Usage: python stop_limit.py SYMBOL SIDE QUANTITY STOP_PRICE LIMIT_PRICE")
    print("Example: python stop_limit.py BTCUSDT SELL 0.001 25000 24900")
    sys.exit(1)

symbol = sys.argv[1].upper()
side = sys.argv[2].upper()
quantity = float(sys.argv[3])
stop_price = float(sys.argv[4])
limit_price = float(sys.argv[5])

# Validate side
if side not in ['BUY', 'SELL']:
    print("❌ SIDE must be BUY or SELL")
    sys.exit(1)

# Validate prices
if stop_price <= 0 or limit_price <= 0 or quantity <= 0:
    print("❌ Stop, limit price, and quantity must be greater than 0.")
    sys.exit(1)

# Place Stop-Limit Order
try:
    order = client.create_order(
        symbol=symbol,
        side=side,
        type='STOP_LOSS_LIMIT',
        quantity=quantity,
        price=str(limit_price),
        stopPrice=str(stop_price),
        timeInForce='GTC'
    )
    logging.info("✅ Stop-Limit Order Placed: %s", json.dumps(order, indent=2))
    print("✅ Stop-Limit order placed successfully.")
except Exception as e:
    logging.error(f"❌ Stop-Limit Order Failed: {e}")
    print(f"❌ Error placing stop-limit order: {e}")
