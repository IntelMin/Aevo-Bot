from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand, BotCommandScopeAllPrivateChats
from keyboards.menu import generate_menu, home_button
from utils.config import BOT_TOKEN, BOT_NAME
from database.db import get_user
from .wallet import *

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

    user_record = get_user(chat_id)
    if user_record:
        print('User exists')
        username = message.from_user.username
        preload_message.edit_text(text=f'Welcome back {username}', reply_markup=home_button())
        return
        
    greeting_message = "Let's get started! 💼\n\n"
    keyboard = generate_menu() 
    
    await preload_message.edit_text(
        text=greeting_message,
        parse_mode='Markdown',
        reply_markup=keyboard
    )
    
@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(
        text = "🚀 *Welcome to {BOT_NAME} on Telegram!* 🚀\n\n",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )
    
@router.callback_query(F.data == "wallet_create")
async def create_wallet(callback: CallbackQuery, state: FSMContext):
    await create_wallet_callback(callback, state)

@router.callback_query(F.data == "wallet_import")
async def import_wallet(callback: CallbackQuery, state: FSMContext):
    await import_wallet_callback(callback, state)

@router.message(WalletStates.setting_wallet)
async def process_import_wallet(message: Message, state: FSMContext):
    await process_import_wallet_callback(message, state)