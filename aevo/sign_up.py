from utils.blockchain import generate_eth_private_key, w3
from eth_account.messages import encode_defunct, _hash_eip191_message
from web3 import constants
from eip712 import EIP712Message, EIP712Type

class Register(EIP712Type):
    key: "address", # type: ignore
    expiry: "uint256" # type: ignore

class Sign_Message(EIP712Message):
    register = Register('', '')


def generate_account_sig():
    private_key = generate_eth_private_key()
    message = encode_defunct( {
      'name': "Aevo Mainnet",
      'version': "1",
      'chainId': 1,
    },
    {
      'Register': [
        { 'name': "key", 'type': "address" },
        { 'name': "expiry", 'type': "uint256" },
      ],
    },
    {
      'key': w3.eth.account.from_key(private_key).address,
      'expiry': str(constants.MAX_INT),
    })
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)
    print('signature: ', signed_message.signature.hex(), signed_message['signature'].hex())
    return signed_message