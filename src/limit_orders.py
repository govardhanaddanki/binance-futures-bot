import os
import sys
import logging
from binance.client import Client
from dotenv import load_dotenv

# Step 1: Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Step 2: Configure logging to bot.log
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Step 3: Connect to Binance Spot Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Step 4: Validate command line arguments
if len(sys.argv) != 5:
    print("Usage: python limit_orders.py SYMBOL SIDE QUANTITY PRICE")
    print("Example: python limit_orders.py BTCUSDT BUY 0.001 25000")
    sys.exit(1)

symbol = sys.argv[1].upper()
side = sys.argv[2].upper()
quantity = float(sys.argv[3])
price = float(sys.argv[4])

# Step 5: Validate side
if side not in ['BUY', 'SELL']:
    print("❌ SIDE must be BUY or SELL")
    sys.exit(1)

# Step 6: Validate that quantity and price are positive
if quantity <= 0 or price <= 0:
    print("❌ Quantity and price must be positive numbers")
    sys.exit(1)

# Step 7: Place the limit order
try:
    order = client.create_order(
        symbol=symbol,
        side=side,
        type='LIMIT',
        quantity=quantity,
        price=str(price),
        timeInForce='GTC'  # GTC = Good Till Cancelled
    )
    logging.info(f"✅ Limit Order Placed: {order}")
    print("✅ Limit order placed successfully.")
except Exception as e:
    logging.error(f"❌ Limit Order Failed: {e}")
    print(f"❌ Error placing limit order: {e}")
