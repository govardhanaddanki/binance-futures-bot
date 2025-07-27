import os
import sys
import logging
from binance.client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Connect to Spot Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Validate CLI args
if len(sys.argv) != 6:
    print("Usage: python oco.py SYMBOL SIDE QUANTITY TAKE_PROFIT STOP_LOSS")
    print("Example: python oco.py BTCUSDT SELL 0.001 30000 22000")
    sys.exit(1)

symbol = sys.argv[1].upper()
side = sys.argv[2].upper()
quantity = float(sys.argv[3])
take_profit_price = float(sys.argv[4])
stop_loss_price = float(sys.argv[5])

if side != 'SELL':
    print("❌ OCO orders are only supported for SELL side on Binance Spot.")
    sys.exit(1)

# Place OCO order
try:
    order = client.create_oco_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=str(take_profit_price),          # Take-Profit limit price
        stopPrice=str(stop_loss_price),        # Stop-Loss trigger
        stopLimitPrice=str(stop_loss_price-100),  # Stop-Loss actual order price
        stopLimitTimeInForce='GTC'
    )
    logging.info(f"✅ OCO Order Placed: {order}")
    print("✅ OCO order placed successfully.")
except Exception as e:
    logging.error(f"❌ OCO Order Failed: {e}")
    print(f"❌ Error placing OCO order: {e}")
