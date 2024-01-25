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
    expiry = str(int(time.time() + (86400 * 365)))
    print(account, signer, account_sig, signer_sig, expiry)
    # url = "https://api.aevo.xyz/register" # Mainnet
    url = "https://api-testnet.aevo.xyz/register" # Testnet
    payload = {
      "account": account,
      "signing_key": signer,
      "expiry": expiry,
      "account_signature": account_sig,
      "signing_key_signature": signer_sig
    }
    res = requests.post(url, json=payload, headers=headers)
    print(res.status_code, res.text)
    if res.status_code == 200:
        data = res.json()
        return data
    return None
    
async def sign_up(private_key):
    address = w3.eth.account.from_key(private_key).address
    payload = {
      "account": address,
      "private_key": private_key
    }
    res = requests.post(API_URL, json=payload, headers=headers)
    print(res.status_code, res.text, 'sign up')
    if res.status_code == 200:
        data = res.json()
        register_data = await register(**data)
        print(register_data)
        return register_data
    return None

if __name__ == "__main__":
    import asyncio
    asyncio.run(sign_up('0x591821a644ea03dc628ac4c6d0e29654858c655fb40d563013ea7b47c2346f86'))