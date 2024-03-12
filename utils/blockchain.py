import secrets
from web3 import Web3
from .config import RPC_URL
# from .abi import abi_manager

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def is_valid_eth_private_key(pk: str):
    pk = pk[2:] if pk.startswith('0x') else pk
    if len(pk) == 64 and pk.isalnum():
        return pk  
    
    return False  

def is_valid_address(address: str):
    return Web3.is_address(address)

def generate_eth_private_key():
    # A private key is a 256-bit number, which can be represented as a 32-byte hexadecimal
    max_hex_value = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140 
    private_key_hex = secrets.randbelow(max_hex_value)  
    
    # Converting the number to a hexadecimal string and ensuring it has a length of 64 characters
    return hex(private_key_hex)[2:].zfill(64)

# def get_eth_balances(wallet_addresses):
#     balances = {}
    
#     # Creating a batch
#     batch = w3.eth.contract().functions.balanceOf('').call.request(
#         block_identifier='latest'
#     ).method
#     batch = [[batch, [address]] for address in wallet_addresses]

#     # Sending the batch request
#     results = w3.eth.sendBatch(batch)
    
#     # Converting the results from Wei to Ether and storing them
#     for address, balance_wei in zip(wallet_addresses, results):
#         balances[address] = w3.fromWei(balance_wei, 'ether')
        
#     return balances