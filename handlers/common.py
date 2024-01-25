from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand, BotCommandScopeAllPrivateChats
from keyboards.menu import generate_menu, home_button, main_menu
from utils.config import BOT_TOKEN, BOT_NAME
from database.db import get_user
from .sign_up import *

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
        greeting_message = "Let's get you started! 💼\n\n"
        keyboard = generate_menu() 
        
        await preload_message.edit_text(
            text=greeting_message,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
    
@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(
        text = f"🚀 *Welcome to {BOT_NAME} on Telegram!* 🚀\n\n",
        parse_mode='Markdown',
        reply_markup=main_menu
    )
    
# Sign Up handlers
@router.callback_query(F.data == "aevo_signup")
async def create_wallet(callback: CallbackQuery, state: FSMContext):
    await sign_up_callback(callback, state)

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
