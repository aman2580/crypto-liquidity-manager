import ccxt
import logging
import time

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# -----------------------------
# Exchange Connection
# -----------------------------
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True
})

# -----------------------------
# Strategy Configuration
# -----------------------------
SYMBOL = 'BTC/USDT'

# Trigger if spread exceeds 2%
TARGET_SPREAD_PERCENT = 2

# Inventory thresholds
MAX_BTC_POSITION = 0.5
MIN_BTC_POSITION = 0.1

# -----------------------------
# Fetch Order Book Data
# -----------------------------
def get_order_book(symbol):
    order_book = exchange.fetch_order_book(symbol)

    best_bid = order_book['bids'][0][0]
    best_ask = order_book['asks'][0][0]

    spread_percent = ((best_ask - best_bid) / best_bid) * 100

    return best_bid, best_ask, spread_percent

# -----------------------------
# Fetch Account Inventory
# -----------------------------
def get_inventory():
    balance = exchange.fetch_balance()

    btc_balance = balance['BTC']['free']
    usdt_balance = balance['USDT']['free']

    return btc_balance, usdt_balance

# -----------------------------
# Liquidity & Inventory Logic
# -----------------------------
def manage_liquidity():

    best_bid, best_ask, spread = get_order_book(SYMBOL)
    btc_balance, usdt_balance = get_inventory()

    logging.info(f"Best Bid: {best_bid}")
    logging.info(f"Best Ask: {best_ask}")
    logging.info(f"Spread: {spread:.4f}%")

    logging.info(f"BTC Inventory: {btc_balance}")
    logging.info(f"USDT Balance: {usdt_balance}")

    # Spread Monitoring Logic
    if spread > TARGET_SPREAD_PERCENT:
        logging.warning(
            "Spread exceeds 2% threshold -> Potential liquidity imbalance detected"
        )

    # Inventory Risk Controls
    if btc_balance > MAX_BTC_POSITION:
        logging.warning(
            "BTC inventory exceeds max threshold -> Rebalancing / hedge required"
        )

    elif btc_balance < MIN_BTC_POSITION:
        logging.warning(
            "BTC inventory below minimum threshold -> Increase inventory levels"
        )

    else:
        logging.info("Inventory levels within acceptable range")

# -----------------------------
# Main Monitoring Loop
# -----------------------------
while True:

    try:
        manage_liquidity()

        # Monitor every 10 seconds
        time.sleep(10)

    except Exception as e:

        logging.error(f"System Error: {e}")

        # Retry delay
        time.sleep(5)

"""
Project Notes:
- Built for monitoring liquidity conditions on crypto CEXs
- Tracks spread behavior and inventory exposure
- Can be extended to multiple exchanges such as Bybit, OKX, Coinbase etc.
- Designed as a lightweight risk monitoring and liquidity management tool
"""
