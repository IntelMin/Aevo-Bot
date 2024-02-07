from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from utils.blockchain import is_valid_eth_private_key, is_valid_address
from database.db import add_user
from keyboards.menu import home_button

from aevo.sign_up import sign_up as sign_up_with_private_key

class WalletStates(StatesGroup):
    setting_wallet = State() 
    setting_signature = State() 
    setting_apikey = State() 
    setting_apisecret = State()
    setting_privatekey = State()

class WalletFactory(CallbackData, prefix="wallet"):
    action: str

sign_up = {}

from aiogram.types import ForceReply
async def sign_up_callback(callback: CallbackQuery, state: FSMContext):    
    await callback.message.answer("Please enter your Trading wallet address",
        reply_markup=ForceReply(selective=True))
    
    await state.set_state(WalletStates.setting_wallet)

async def wallet_callback(message: Message, state: FSMContext):
    
    user_id = message.from_user.id
    wallet = message.text.strip()

    if is_valid_address(wallet):
        sign_up[user_id] = {'wallet_address': wallet}

        await message.answer("Please enter your Signature key of the trading wallet you are importing.",
            reply_markup=ForceReply(selective=True))

        await state.set_state(WalletStates.setting_signature)
    else:
        await message.answer("Please enter a valid wallet address")
    
async def signature_callback(message: Message, state: FSMContext):
    
    user_id = message.from_user.id
    signature = message.text.strip()  # Getting the private key from the user’s message
    
    if is_valid_eth_private_key(signature):
        sign_up[user_id].update({'signing_key': signature})

        await message.answer("Please enter your API Key of the trading wallet you are importing.",
            reply_markup=ForceReply(selective=True))

        await state.set_state(WalletStates.setting_apikey)
    else:
        await message.answer("Please enter a valid signature key")

async def apikey_callback(message: Message, state: FSMContext):
    user_id = message.from_user.id
    apikey = message.text.strip()  # Getting the private key from the user’s message

    sign_up[user_id].update({'api_key': apikey})

    await message.answer("Please enter your API Secret of the trading wallet you are importing.",
        reply_markup=ForceReply(selective=True))

    await state.set_state(WalletStates.setting_apisecret)

async def apisecret_callback(message: Message, state: FSMContext):
    user_id = message.from_user.id
    apisecret = message.text.strip()

    sign_up[user_id].update({'api_secret': apisecret})

    if await validate_api_key_and_secret(user_id):
        res = await message.answer("Aevo sign up complete. Updating details...")
        add_user(user_id, sign_up[user_id])

        await res.answer(
            (
                f"Wallet address: `{sign_up[user_id]['wallet_address']}`\n"
                f"✅ Account loaded successfully!\n\n"
            ),
            parse_mode='Markdown',
            reply_markup=home_button
        )

    else:
        await message.answer("We couldn't validate your API key and secret. Please try again or contact our support for assistance")
        await state.set_state(WalletStates.setting_apikey)


async def sign_up_private_key_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Please enter your Private key\nThis will be encrypted on our servers and will not be shared with anyone.",
        reply_markup=ForceReply(selective=True), parse_mode='Markdown')
    
    await state.set_state(WalletStates.setting_privatekey)

async def private_key_callback(message: Message, state: FSMContext):
    user_id = message.from_user.id
    private_key = message.text.strip()

    if is_valid_eth_private_key(private_key):
        data = await sign_up_with_private_key(private_key)
        if 'error' in data:
            await message.answer(f"There was an error parsing your request\n`{data['error']}`\n\nCall /start to begin anew", parse_mode='Markdown')
            return
        
        sign_up[user_id] = data
        if await validate_api_key_and_secret(user_id):
            res = await message.answer("Aevo sign up complete. Updating details...")
            add_user(user_id, sign_up[user_id])

            await res.answer(
                (
                    f"Wallet address: `{sign_up[user_id]['wallet_address']}`\n"
                    f"✅ Account loaded successfully!\n\n"
                ),
                parse_mode='Markdown',
                reply_markup=home_button
            )
        else:
            await message.answer("We couldn't process your sign up. Please try again or contact our support for assistance\n\n/start")

        
    else:
        await message.answer("Please enter a valid private key",
        reply_markup=ForceReply(selective=True), parse_mode='Markdown')
        await state.set_state(WalletStates.setting_privatekey)

async def validate_api_key_and_secret(user_id):
    import requests

    url = "https://api.aevo.xyz/auth"
    # url = "https://api-testnet.aevo.xyz/auth" # Testnet

    key = sign_up[user_id]['api_key']
    secret = sign_up[user_id]['api_secret']

    headers = {
        "accept": "application/json",
        "AEVO-KEY": key,
        "AEVO-SECRET": secret
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    if response.status_code == 200:
        return True
    else:
        return False