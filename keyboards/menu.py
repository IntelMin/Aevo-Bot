import re
from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import Optional

router = Router()

class MenuFactory(CallbackData, prefix="trade"):
    action: str
    process: Optional[str] = None
    subject: Optional[str] = None

def generate_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="----- Set up Aevo Account -----", callback_data='filler')
    markup.button(text="Create Wallet", callback_data="wallet_:create")
    markup.button(text="Import Wallet", callback_data="wallet_:import")

    markup.adjust(1, 2)
    return markup.as_markup()

def home_button():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = KeyboardButton('📍Account')
    item2 = KeyboardButton('⚡Assets')
    item3 = KeyboardButton('💹Trade')
    item4 = KeyboardButton('📊Funding')
    item5 = KeyboardButton('📈Price')
    markup.add(item1,item2,item3,item4, item5)

    return markup