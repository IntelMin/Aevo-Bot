from utils.hash import encrypt, decrypt
from json import dumps


text_to_encrypt = dumps({"hello": "world"})

print(encrypt(text_to_encrypt))