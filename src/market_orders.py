import os
import sys
import logging
from binance.client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Connect to Binance Spot Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'  # ✅ Spot Testnet URL

# Validate CLI arguments
if len(sys.argv) != 4:
    print("Usage: python market_orders.py SYMBOL SIDE QUANTITY")
    print("Example: python market_orders.py BTCUSDT BUY 0.01")
    sys.exit(1)

symbol = sys.argv[1].upper()
side = sys.argv[2].upper()
quantity = float(sys.argv[3])

if side not in ['BUY', 'SELL']:
    print("❌ SIDE must be BUY or SELL")
    sys.exit(1)

# Place market order (on Spot Testnet)
try:
    order = client.create_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=quantity
    )
    logging.info(f"✅ Market Order Placed: {order}")
    print("✅ Market order placed successfully.")
except Exception as e:
    logging.error(f"❌ Market Order Failed: {e}")
    print(f"❌ Error placing market order: {e}")
