import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
BOT_NAME = os.getenv("BOT_NAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
RPC_URL = os.getenv("RPC_URL")
REDIS_URL = os.getenv("REDIS_URL")
API_URL = os.getenv("API_URL")
BOT_CONTRACT = os.getenv("BOT_CONTRACT")