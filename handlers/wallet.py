from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from utils.blockchain import w3, is_valid_eth_private_key, generate_eth_private_key
from utils.config import BOT_NAME
from database.db import add_user
from aevo.sign_up import sign_up

router = Router()
router.message.filter(F.chat.type == "private")

class WalletStates(StatesGroup):
    setting_wallet = State() # Will be represented in storage as 'WalletStates:setting_wallet'

class WalletFactory(CallbackData, prefix="wallet"):
    action: str

async def create_wallet_callback(callback: CallbackQuery, state: FSMContext):
    print("Creating wallet...")
    
    user_id = callback.from_user.id
    
    preload_message = await callback.message.answer("Generating wallet...")

    private_key = generate_eth_private_key()
    address = w3.eth.account.from_key(private_key).address
    
    await preload_message.edit_text("⏳ Processing Aevo signup...")
    # Process Aevo Sign up and get keys
    sign_up_data = await sign_up(f'0x{private_key}')
    if sign_up_data is None:
        await preload_message.edit_text("❌ Aevo sign up failed. Please try again later orcontact our support for assistance")
        return
    
    # Saving the wallet to the database
    add_user(user_id, sign_up_data)
    
    await preload_message.edit_text("⏳ Sign up complete. Updating details...")

    await preload_message.edit_text(
        (
            f"✅ Wallet generated successfully!\n\n"
            f"✨ **New Wallet:**\n`{address}`\n\n"
            f"🔒 **Private Key:**\n`0x{private_key}`\n\n"
            "Properly store your private key in a safe place. You will need it to access your wallet."
            f"Your Signature key, API Key and Secret"
        ),
        parse_mode='Markdown'
    )


from aiogram.types import ForceReply

async def import_wallet_callback(callback: CallbackQuery, state: FSMContext):
    print("Importing wallet...")
    
    await callback.message.answer(
        "Please enter the private key of the wallet you want to import. Make sure the private key is correct and kept secure.",
        reply_markup=ForceReply(selective=True),
    )
    
    # await WalletStates.setting_wallet.set()
    await state.set_state(WalletStates.setting_wallet)

async def process_import_wallet_callback(message: Message, state: FSMContext):
    
    user_id = message.from_user.id
    private_key = message.text.strip()  # Getting the private key from the user’s message
    
    processing_message = await message.answer("⏳ Processing your private key...")
    
    valid_key = is_valid_eth_private_key(private_key)
    
    if valid_key:
        
        await processing_message.edit_text("⏳ Validating and importing wallet...")
        
        # Encrypting and hashing the private key
        wallet_address = w3.eth.account.from_key(private_key).address

        # Saving the wallet to the database
        add_user(user_id, valid_key)
    
        await processing_message.edit_text(
            (
                "✅ Wallet imported successfully!\n\n"
                f"✨ **Wallet Address:**\n`{wallet_address}`\n\n"
                f"You can now interact with {BOT_NAME} using this wallet."
            ),
            parse_mode='Markdown' )
        
    else:
        await processing_message.edit_text(
            "❌ Invalid ETH private key. Please ensure the private key is correct and try again.")
