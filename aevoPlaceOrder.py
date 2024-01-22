from Aevo_SDK.AlethieumAevoSDK import AevoClient
# from clientConfig import clientConfig

from utils.logger import Logger

log = Logger("Aevo Bot")

### CLIENT CONFIG ###
# # Description: Please add your API key and secret to the clientConfig file.
# # Description: In the Readme.md file, you will find instructions on how to create an API key and secret.

clientConfig = {
    'signing_key': '',
    'wallet_address': '',
    'api_key': '',
    'api_secret': '',
    'env': '',
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