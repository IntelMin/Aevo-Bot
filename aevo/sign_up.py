import requests
import time
from utils.config import API_URL
from utils.blockchain import w3

cache = {}

headers = {
  "accept": "application/json",
  "content-type": "application/json"
}
async def register(account, signer, account_sig, signer_sig):
    # url = "https://api.aevo.xyz/register" # Mainnet
    url = "https://api-testnet.aevo.xyz/register" # Testnet
    payload = {
      "account": account,
      "signing_key": signer,
      "expiry": int(time.time() + (86400 * 365)),
      "account_signature": account_sig,
      "signing_key_signature": signer_sig
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()
    
    return data
async def sign_up(private_key):
    address = w3.eth.account.from_key(private_key).address
    payload = {
      "account": address,
      "private_key": private_key
    }
    res = requests.get(API_URL, json=payload, headers=headers)
    data = res.json()