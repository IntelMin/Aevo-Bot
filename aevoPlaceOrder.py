from Aevo_SDK.AlethieumAevoSDK import AevoClient
from utils.config import *

from utils.logger import Logger

log = Logger("Aevo Bot")


clientConfig = {
    'signing_key': SIGNING_KEY,
    'wallet_address': WALLET_ADDRESS,
    'api_key': API_KEY,
    'api_secret': API_SECRET,
    'env': 'testnet',
}

# Add Credentials
aevo = AevoClient(**clientConfig)

# Create a market order
order_params = {
    "instrument_id": '' ,  # Instrument ID number
    "is_buy": '' , # True for long order, false for short order
    "quantity": '',    # Number of contracts. In 6 decimals fixed number
}

order = aevo.rest_create_market_order(**order_params)
log.info(f"Order: {order}")