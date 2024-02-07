import requests
import time
from utils.config import RPC_URL

from eth_account.messages import encode_structured_data
from eth_account.datastructures import SignedMessage
from eth_account import Account
from web3 import AsyncWeb3
from web3.eth import AsyncEth


def get_signatures(
        web3: AsyncWeb3,
        wallet_address: str,
        account: Account
) -> tuple[str, SignedMessage, str, str]:
    new_acc = web3.eth.account.create()
    signing_key = new_acc.address
    signing_private = new_acc.key.hex()

    register_data = {
        "name": "Aevo Mainnet",
        "version": "1",
        "chainId": 1
    }
    register_types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"}
        ],
        "Register": [
            {"name": "key", "type": "address"},
            {"name": "expiry", "type": "uint256"}
        ],

    }
    register_values = {
        "key": signing_key,
        "expiry": int(time.time() + 10000)
    }
    register_structured_data = {
        "types": register_types,
        "primaryType": "Register",
        "domain": register_data,
        "message": register_values
    }

    msg = encode_structured_data(register_structured_data)
    account_signature = account.sign_message(msg).signature.hex()

    signing_key_signature = web3.eth.account.sign_typed_data(
        domain_data={
            "name": "Aevo Mainnet",
            "version": "1",
            "chainId": 1,
        },
        message_types={
            "SignKey": [
                {"name": "account", "type": "address"}
            ]
        },
        message_data={
            "account": wallet_address
        },
        private_key=signing_private

    )
    signing_key_signature = signing_key_signature.signature.hex()

    return signing_key, account_signature, signing_key_signature, signing_private


headers = {
  "accept": "application/json",
  "content-type": "application/json"
}
async def register(account, signer, account_sig, signer_sig):
    url = "https://api.aevo.xyz/register" # Mainnet
    # url = "https://api-testnet.aevo.xyz/register" # Testnet
    payload = {
      "account": account,
      "account_signature": account_sig,
      "expiry": int(time.time() + 10000),
      "signing_key": signer,
      "signing_key_signature": signer_sig
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()
        return data
    return None
    
async def sign_up(private_key):
    w3 = AsyncWeb3(
            provider=AsyncWeb3.AsyncHTTPProvider(
                endpoint_uri=RPC_URL,
            ),
            modules={'eth': (AsyncEth,)},
            middlewares=[]
        )
    account: Account = w3.eth.account.from_key(private_key)
    wallet_address = account.address

    signer, account_sig, signer_sig, signing_key = get_signatures(w3, wallet_address, account)
    data = await register(wallet_address, signer, account_sig, signer_sig)
    if data is None:
        return {'error': 'An error occurred while trying to sign up'}
    
    result = {'wallet_address': wallet_address, 'signing_key': signing_key, 'api_key': data['api_key'], 'api_secret': data['api_secret']}
    return result
