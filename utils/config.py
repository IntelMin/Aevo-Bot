import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
BOT_NAME = os.getenv("BOT_NAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SIGNING_KEY = os.getenv("SIGNING_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
RPC_URL = os.getenv("RPC_URL")