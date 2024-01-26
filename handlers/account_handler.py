from aiogram.types import Message,  ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.db import get_user
from keyboards.menu import home_button
from utils.response.account_response import *
from Aevo_SDK.AlethieumAevoSDK import AevoClient


async def account(callback: CallbackQuery):
    request = callback.data.split(':')[1]
    user_id = callback.from_user.id
    user:dict = get_user(user_id)
    aevo = AevoClient(**user)

    res = callback.message.answer

    if request == 'portfolio':
        response = aevo.rest_get_portfolio()
        if 'error' in response:
            await message.answer(f"There was an error processing this request\n{response['error']}", reply_markup=home_button)
            return
        message = respond_to_portfolio_request(response)
        await res(message, reply_markup=home_button)
        
    elif request == 'positions':
        response = aevo.rest_get_positions()
        if 'error' in response:
            await message.answer(f"There was an error processing this request\n{response['error']}", reply_markup=home_button)
            return
        message = respond_to_account_positions(response)
        await res(message, reply_markup=home_button)

    elif request == 'order_history':
        response = aevo.rest_get_order_history()
        if 'error' in response:
            await res(f"There was an error processing this request\n{response['error']}")
            return
        message = respond_to_order_history(response)
        await res(message, reply_markup=home_button)
    
    elif request == 'trade_history':
        response = aevo.rest_get_trade_history()
        if 'error' in response:
            await res(f"There was an error processing this request\n{response['error']}")
            return
        message = respond_to_trade_history(response)
        await res(message, reply_markup=home_button)
