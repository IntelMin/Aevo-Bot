from aiogram.types import Message,  ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.db import get_user
from database.cache import *
from keyboards.menu import home_button, two_way_button
from utils.response.trade_response import  *
from Aevo_SDK.AlethieumAevoSDK import AevoClient

class TradeState(StatesGroup):
    setting_order = State() 
    setting_order_edit = State() 


async def trade(callback: CallbackQuery, state: FSMContext):
    request = callback.data.split(':')[1]
    user_id = callback.from_user.id
    user:dict = get_user(user_id)
    aevo = AevoClient(**user)

    res = callback.message.answer

    if request == 'market_order' or request == 'limit_order':
        add_trade_cache(user_id, 'request', request)
        await res('Please enter the name of the asset you wish to trade', reply_markup=ReplyKeyboardRemove())
        await state.set_state(TradeState.setting_order)

    elif request == 'edit_order' or request == 'cancel_order':
        add_trade_cache(user_id, 'request', request)
        action = 'edit' if request == 'edit_order' else 'cancel'
        await res(f'Please enter the order_id of the order you wish to {action}', reply_markup=ReplyKeyboardRemove())
        await state.set_state(TradeState.setting_order_edit)

    elif request == 'view_orders':
        response = aevo.rest_get_open_orders()
        if 'error' in response:
            await res(f"There was an error processing this request\n{response['error']}")
            return
        message = respond_to_open_orders(response)
        await res(message, reply_markup=home_button)
    
    elif request == 'cancel_orders':
        response = aevo.rest_cancel_all_orders()
        if 'error' in response:
            await res(f"There was an error processing this request\n{response['error']}")
            return
        await res("All active orders on this account has been cancelled", reply_markup=home_button)

async def handle_order_edits(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user:dict = get_user(user_id)
    aevo = AevoClient(**user)

    order_id = message.text.strip()
    request = get_trade_cache(user_id, 'request')

    if request == 'edit_order':
        return # There is a lot of gray area on how this should be handled
        # order = aevo.rest_get_open_order(order_id)
        # if 'error' in order:
        #     delete_trade_cache(user_id)
        #     await message.answer(f"There was an error processing this request\n{order['error']}", reply_markup=home_button)
        #     return
        # add_trade_cache(user_id, 'instrument_id', order['instrument_id'])
        # add_trade_cache(user_id, 'is_buy', order['side'])
        # add_trade_cache(user_id, 'order_id', order_id)
        # await message.answer('Please enter the name of the asset you wish to trade', reply_markup=ReplyKeyboardRemove())
        # await state.set_state(TradeState.setting_order)
    else:
        response = aevo.rest_cancel_order(order_id)
        if 'error' in response:
            await message.answer(f"There was an error processing this request\n{response['error']}", reply_markup=home_button)
            return
        await message.answer(f"Order with order_id: {order_id} has been cancelled successfully", reply_markup=home_button)

async def handle_orders(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user:dict = get_user(user_id)
    aevo = AevoClient(**user)

    user_input = message.text.strip().upper()
    request = get_trade_cache(user_id, 'request')

    if get_trade_cache(user_id, 'instrument_id') is None:
        response = aevo.get_instrument(user_input)
        if 'error' in response:
            delete_trade_cache(user_id)
            await message.answer(f"There was an error processing this request\n{response['error']}", reply_markup=home_button)
            return
        add_trade_cache(user_id, 'instrument_id', response['instrument_id'])
        add_trade_cache(user_id, 'asset', user_input)
        await message.answer(f'Price of {user_input} ({response["instrument_name"]}) is ${response["index_price"]}\nPlease enter what trade direction the order should take? (Buy/Sell)', reply_markup=two_way_button())
        await state.set_state(TradeState.setting_order)

    elif get_trade_cache(user_id, 'is_buy') is None:
        _input = False if user_input.lower() == "sell" else True
        add_trade_cache(user_id, 'is_buy', _input)
        asset = get_trade_cache(user_id, 'asset')
        res_text = f"You have selected {user_input} as trade direction\n"
        res_text +=  f"Please enter the limit price to {user_input} {asset}" if request == 'limit_order' else f"Please enter the quantity of {asset} to {user_input}"
        await message.answer(res_text, reply_markup=ReplyKeyboardRemove())
        await state.set_state(TradeState.setting_order)

    elif get_trade_cache(user_id, 'limit_price') is None and request == 'limit_order':
        _input = float(user_input)
        add_trade_cache(user_id, 'limit_price', _input)
        asset = get_trade_cache(user_id, 'asset')
        is_buy = get_trade_cache(user_id, 'is_buy')
        _trade = 'buy' if is_buy else 'sell'
        res_text = f"Limit price set to ${user_input}\n"
        res_text +=  f"Please enter the quantity of {asset} to {_trade}"
        await message.answer(res_text)
        await state.set_state(TradeState.setting_order)

    elif get_trade_cache(user_id, 'quantity') is None:
        _input = float(user_input)
        add_trade_cache(user_id, 'quantity', _input)
        res_text = process_trade_cache(user_id)
        await message.answer(res_text, reply_markup=two_way_button("Yes", "No"))
        await state.set_state(TradeState.setting_order)

    else:
        if user_input.lower() == 'no':
            delete_trade_cache(user_id)
            await message.answer("Your Order has been successfully cancelled", reply_markup=home_button)
            return
        data = None
        aevo_trade_data = get_trade_cache_data(user_id)
        
        if request == 'market_order':
            data = aevo.rest_create_market_order(**aevo_trade_data)
        else:
            data = aevo.rest_create_order(**aevo_trade_data)
        if 'error' in data:
            delete_trade_cache(user_id)
            await message.answer(f"There was an error processing your trade request\n{data['error']}", reply_markup=home_button)
            return
        res_text = f"Here are your order details \n\n"
        res_text += process_order_data(data)
        delete_trade_cache(user_id)
        await message.answer(res_text, reply_markup=home_button)
            

    