import secrets
from web3 import Web3, constants
from utils.config import RPC_URL, SIGNING_KEY
from aevo.sign_up import generate_account_sig
# from .abi import abi_manager

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def tf(key):
    return w3.eth.account.from_key(key).address

print(generate_account_sig())