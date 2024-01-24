import re
from aiogram import F, Router, types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import Optional

router = Router()

class MenuFactory(CallbackData, prefix="trade"):
    action: str
    process: Optional[str] = None
    subject: Optional[str] = None

def generate_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="----- Wallet -----", callback_data='filler')
    markup.button(text="💼 Create", callback_data="wallet_create")
    markup.button(text="📤 Import", callback_data="wallet_import")
    markup.button(text="🗑️ Delete", callback_data="wallet_delete")

    markup.adjust(1, 3)
    return markup.as_markup()

def generate_new_user_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="💼 Create", callback_data="wallet_create")
    markup.button(text="📤 Import", callback_data="wallet_import")
    markup.adjust(2)
    return markup.as_markup()
