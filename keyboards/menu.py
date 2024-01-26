from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import Optional

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

def two_way_button(b1 = "Buy", b2 = "Sell"):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=b1),
            KeyboardButton(text=b2), 
        ]
    ], 
    resize_keyboard=True,
    input_field_placeholder='Please select from Button below'
    )

def account_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="View Portfolio", callback_data='aevo_account:portfolio')
    markup.button(text="View Positions", callback_data='aevo_account:positions')
    markup.button(text="Order History", callback_data='aevo_account:order_history')
    markup.button(text="Trade History", callback_data='aevo_account:trade_history')
    markup.adjust(2,2)
    return markup.as_markup()

def trade_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="Create Market Order", callback_data='aevo_trade:market_order')
    markup.button(text="Create Limit Order", callback_data='aevo_trade:limit_order')
    markup.button(text="View Open Orders", callback_data='aevo_trade:view_orders')
    markup.button(text="Edit Order", callback_data='aevo_trade:edit_order')
    markup.button(text="Cancel An Order", callback_data='aevo_trade:cancel_order')
    markup.button(text="Cancel All Orders", callback_data='aevo_trade:cancel_orders')
    markup.adjust(2,2,2)
    return markup.as_markup()