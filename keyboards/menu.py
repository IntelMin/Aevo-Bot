import re
from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,  ReplyKeyboardRemove
from typing import Optional

router = Router()

class MenuFactory(CallbackData, prefix="trade"):
    action: str
    process: Optional[str] = None
    subject: Optional[str] = None

def generate_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="----- Set up Aevo Account -----", callback_data='aevo_signup')

    markup.adjust(1)
    return markup.as_markup()


home_button = ReplyKeyboardMarkup(
keyboard=[
    [
        KeyboardButton(text="📍Account"),
        KeyboardButton(text="⚡Assets"), 
        KeyboardButton(text="💹Trade")
    ],
    [
        KeyboardButton(text="📊Funding"), 
        KeyboardButton(text="📈Price"), 
        KeyboardButton(text="🚸Tutorial")
    ]
], 
resize_keyboard=True,
input_field_placeholder='Make a selection'
)

