from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.menu import *
from utils.config import BOT_NAME
from utils.response.responses import new_user
from database.db import get_user
from database.cache import add_message_entry, delete_trade_cache

from .sign_up import *
from .menu_handler import *
from .account_handler import account
from .trade_handler import *
from .get_Info import *

router = Router()
router.message.filter(F.chat.type == "private")

async def set_bot_commands(bot: Bot):
    
    # commands = [
    #         BotCommand(command="help", description="All available commands"),
    #         BotCommand(command="wallet", description="Set your wallet"),
    #         BotCommand(command="buy", description="Buy tokens"),
    #         BotCommand(command="sell", description="Sell tokens"),
    #         BotCommand(command="top", description="See trending tokens"),
    # ]
    # await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    
    return True
    

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    preload_message = await message.answer("Loading bot...")
    
    await state.clear()

    chat_id = message.from_user.id
    username = message.from_user.username
    username = username if username else 'user'

    user_record = get_user(chat_id)
    if user_record:
        await message.answer(text=f'Welcome back {username}', reply_markup=home_button)
        
    else:    
        greeting_message = new_user(username)
        keyboard = generate_menu() 
        
        await preload_message.edit_text(
            text=greeting_message,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
    
@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):

    preload_message = await message.answer(f"🚀 *Welcome to {BOT_NAME} on Telegram!* 🚀\n\n")
    
    await state.clear()

    username = message.from_user.username
    username = username if username else 'user'

    greeting_message = "You can know here how to get wallet address, SignIngKey, ApiKey and ApiSecret 💼\n\n"
    keyboard = help_menu() 
    
    await preload_message.edit_text(
        text=greeting_message,
        parse_mode='Markdown',
        reply_markup=keyboard
    )

# Get Key handlers
@router.callback_query(F.data == "get_key")
async def get_info(callback: CallbackQuery, state: FSMContext):
    await get_info_callback(callback, state)           
@router.callback_query(F.data == "get_signin_key")
async def get_signinKey(callback: CallbackQuery, state: FSMContext):
    await get_signinKey_callback(callback, state)   
@router.callback_query(F.data == "get_api_info")
async def get_api(callback: CallbackQuery, state: FSMContext):
    await get_api_callback(callback, state)   

# Sign Up handlers
@router.callback_query(F.data == "aevo_signup")
async def create_wallet(callback: CallbackQuery, state: FSMContext):
    await sign_up_callback(callback, state)

@router.callback_query(F.data == "privatekey_signup")
async def create_wallet(callback: CallbackQuery, state: FSMContext):
    await sign_up_private_key_callback(callback, state)

@router.message(WalletStates.setting_wallet)
async def process_wallet_callback(message: Message, state: FSMContext):
    await wallet_callback(message, state)

@router.message(WalletStates.setting_signature)
async def process_signature_callback(message: Message, state: FSMContext):
    await signature_callback(message, state)

@router.message(WalletStates.setting_apikey)
async def process_apikey_callback(message: Message, state: FSMContext):
    await apikey_callback(message, state)

@router.message(WalletStates.setting_apisecret)
async def process_apisecret_callback(message: Message, state: FSMContext):
    await apisecret_callback(message, state)

@router.message(WalletStates.setting_privatekey)
async def process_privatekey_callback(message: Message, state: FSMContext):
    await private_key_callback(message, state)


# Menu Handler    
@router.message(F.text.in_({'📊Funding', '📈Price'}))
async def handle_funding_and_price(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if get_user(user_id) is None:
        await message.answer("Please set up your account first", reply_markup=generate_menu())
        return
    entry = message.text[1:].lower()
    add_message_entry(user_id, entry)
    await message.answer(f"Please provide the short name symbol of the cryptocurrency you want to check {entry} rates for on Aevo platform (e.g. BTC for Bitcoin, ETH for Ethereum, etc.)", reply_markup=ReplyKeyboardRemove())
    # await state.set_data({'entry': entry})
    await state.set_state(MenuState.home_state)

@router.message(F.text =='🚸Tutorial')
async def handle_tutorial(message: Message, state: FSMContext):
    await message.answer("Please stick around for our tutorial video on how to use this bot.")

@router.message(F.text.in_({'📍Account', '💹Trade'}))
async def handle_account(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    username = username if username else 'user'
    if get_user(user_id) is None:
        await message.answer("Please set up your account first", reply_markup=generate_menu())
        return
    request = message.text[1:].lower()
    if request == 'account':
        await message.answer(f"Hello {username}, welcome to your account.\nPlease select an option from the menu below.", reply_markup=account_menu())
    else:
        delete_trade_cache(user_id)
        await message.answer(f"Hello {username}, welcome to the trade modal.\nPlease select an option from the menu below.", reply_markup=trade_menu())

@router.message(F.text ==  '⚡Assets')
async def send_assets(message: Message):
    await message.answer("We are collecting data, please wait...")
    all_data = await get_alldata()
    new_data = "\n".join(f"{i + 1}) {item}" for i, item in enumerate(all_data, start=0))
    if all_data:
        await message.answer(new_data)
    else:
        await message.answer("Oops, something went wrong. Try again!")

# Account and Trade Handler
@router.callback_query(F.data.startswith("aevo_account:"))
async def handle_account_callback(callback: CallbackQuery, state: FSMContext):
    await account(callback)

@router.callback_query(F.data.startswith("aevo_trade:"))
async def handle_trade_callback(callback: CallbackQuery, state: FSMContext):
    await trade(callback, state)

@router.message(TradeState.setting_order)
async def handle_orders_callback(message: Message, state: FSMContext):
    try:
        await handle_orders(message, state)
    except Exception as e:
        print(e)
        await message.answer(f"An error occured while processing your request\n`{e}`", reply_markup=home_button, parse_mode='Markdown')

@router.message(TradeState.setting_order_edit)
async def handle_order_edits_callback(message: Message, state: FSMContext):
    await handle_order_edits(message, state)

@router.message(TradeState.setting_edit_order)
async def handle_edit_order_callback(message: Message, state: FSMContext):
    try:
        await handle_edit_order(message, state)
    except Exception as e:
        print(e)
        await message.answer(f"An error occured while processing your request\n`{e}`", reply_markup=home_button, parse_mode='Markdown')

@router.message(TradeState.setting_gridbot)
async def handle_grid_callback(message: Message, state: FSMContext):
    try:
        await handle_grid_bot(message, state)
    except Exception as e:
        print(e)
        await message.answer(f"An error occured while processing your Grid Bot\n`{e}`", reply_markup=home_button, parse_mode='Markdown')

@router.message(MenuState.home_state)
async def handle_all(message: Message, state: FSMContext):
    await menu(message)

