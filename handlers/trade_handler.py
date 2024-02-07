from aiogram.types import Message,  ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.db import get_user
from database.cache import *
from keyboards.menu import home_button, two_way_button
from utils.response.trade_response import  *
from Aevo_SDK.AlethieumAevoSDK import AevoClient

import asyncio
import json
import pendulum
import time
import numpy as np
from utils.logger import Logger

logger = Logger("Grid Bot", "INFO")
class TradeState(StatesGroup):
    setting_order = State() 
    setting_order_edit = State() 
    setting_edit_order = State() 
    setting_gridbot = State()


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

    elif request == "grid_bot":
        await res('Please enter the name of the asset you wish to set up a Grid bot for', reply_markup=ReplyKeyboardRemove())
        await state.set_state(TradeState.setting_gridbot)

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
        await res(message, reply_markup=home_button, parse_mode='Markdown')
    
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
        order = aevo.rest_get_open_order(order_id)
        if 'error' in order:
            delete_trade_cache(user_id)
            await message.answer(f"There was an error processing this request\n{order['error']}", reply_markup=home_button)
            return
        elif order['order_status'] != 'opened':
            delete_trade_cache(user_id)
            await message.answer(f"The order with id {order_id} is not active", reply_markup=home_button)
            return
        add_trade_cache(user_id, 'order_id', order_id)
        add_trade_cache(user_id, 'instrument_id', order['instrument_id'])
        is_buy = True if order['side'] == 'buy' else False
        add_trade_cache(user_id, 'is_buy', is_buy)
        await message.answer(f"Order with id {order_id} is active\nInitial Limit Price: {order['price']}\nInitial Order Size: {order['amount']}\n\nPlease enter the new limit price", reply_markup=ReplyKeyboardRemove())
        await state.set_state(TradeState.setting_edit_order)
        
    else:
        response = aevo.rest_cancel_order(order_id)
        if 'error' in response:
            await message.answer(f"There was an error processing this request\n{response['error']}", reply_markup=home_button)
            return
        res = f"Order has been cancelled successfully\nBelow were the Order details\n\n"
        res+=process_order_data(response)
        await message.answer(res, reply_markup=home_button)

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
        await message.answer(f'Price of {user_input} ({response["instrument_name"]}) is ${response["index_price"]}\nMinimum Order Value: {response["min_order_value"]}\nMaximum Order Value: {response["max_order_value"]}\n\n Please enter what trade direction the order should take? (Buy/Sell)', reply_markup=two_way_button())
        await state.set_state(TradeState.setting_order)

    elif get_trade_cache(user_id, 'is_buy') is None:
        _input = False if user_input.lower() == "sell" else True
        add_trade_cache(user_id, 'is_buy', _input)
        asset = get_trade_cache(user_id, 'asset')
        dir = 'Buy' if _input else "Sell"
        res_text = f"You have selected {dir} as trade direction\n"
        res_text +=  f"Please enter the limit price to {dir} {asset}" if request == 'limit_order' else f"Please enter the quantity of {asset} to {dir}"
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
            await message.answer(f"There was an error processing your trade request 🥹\n{data['error']}", reply_markup=home_button)
            return
        res_text = f"Order is Successful 🎉 \nHere are your order details \n\n"
        res_text += process_order_data(data)
        delete_trade_cache(user_id)
        await message.answer(res_text, reply_markup=home_button, parse_mode='Markdown')
            

async def handle_edit_order(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user:dict = get_user(user_id)
    aevo = AevoClient(**user)

    user_input = message.text.strip().upper()
    
    if get_trade_cache(user_id, 'limit_price') is None:
        _input = float(user_input)
        add_trade_cache(user_id, 'limit_price', _input)
        res_text = f"Limit price is set to ${_input}\n"
        res_text +=  f"Please enter the new Order Size"
        await message.answer(res_text)
        await state.set_state(TradeState.setting_edit_order)

    elif get_trade_cache(user_id, 'quantity') is None:
        _input = float(user_input)
        add_trade_cache(user_id, 'quantity', _input)
        res_text = process_trade_edit_cache(user_id)
        await message.answer(res_text, reply_markup=two_way_button("Yes", "No"))
        await state.set_state(TradeState.setting_edit_order)

    else:
        if user_input.lower() == 'no':
            delete_trade_cache(user_id)
            await message.answer("Your Order Edit request has been successfully cancelled", reply_markup=home_button)
            return
        
        aevo_trade_data = get_trade_cache_data(user_id)
        data = aevo.rest_edit_order(**aevo_trade_data)
        if 'error' in data:
            delete_trade_cache(user_id)
            await message.answer(f"There was an error processing your order edit request 🥹\n{data['error']}", reply_markup=home_button)
            return
        res_text = f"Order has been Successfully updated 🎉 \nHere are your new order details \n\n"
        res_text += process_order_data(data)
        delete_trade_cache(user_id)
        await message.answer(res_text, reply_markup=home_button, parse_mode='Markdown')
            
async def handle_grid_bot(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user:dict = get_user(user_id)
    aevo = AevoClient(**user)

    user_input = message.text.strip().upper()

    if get_trade_cache(user_id, 'instrument_id') is None:
        response = aevo.get_instrument(user_input)
        if 'error' in response:
            delete_trade_cache(user_id)
            await message.answer(f"There was an error processing this request\n{response['error']}", reply_markup=home_button)
            return
        add_trade_cache(user_id, 'instrument_id', response['instrument_id'])
        add_trade_cache(user_id, 'instrument_name', response['instrument_name'])
        add_trade_cache(user_id, 'asset', user_input)
        await message.answer(f' Please enter the Order size for the Grid Bot configuration\n\nThis determines how much {user_input} the bot will buy or sell in each trade')
        await state.set_state(TradeState.setting_gridbot)

    elif get_trade_cache(user_id, 'order_size') is None:
        _input = float(user_input)
        add_trade_cache(user_id, 'order_size', _input)
        asset = get_trade_cache(user_id, "asset")
        await message.answer(f"Order size has been set.\nBot will continuously trade {_input} {asset} in each transaction\n\nPlease enter a vlaue for Grid size\nThis sets the distance between each price level where the bot will place buy and sell orders.\nFor example, if Grid Size is set to 10, the bot will place buy and sell orders at price levels that are $10 apart.")
        await state.set_state(TradeState.setting_gridbot)

    elif get_trade_cache(user_id, 'grid_size') is None:
        _input = float(user_input)
        add_trade_cache(user_id, 'grid_size', _input)
        await message.answer(f'Grid size is set at {_input}\nProceed to set Grid Lines\nThis represents the total number of grid lines or levels that the bot will create within its trading range. Each grid line represents a price level at which the bot will place a buy or sell order.\nFor example, if Grid Lines is set to 10, the bot will create 10 grid levels within its specified trading range.')
        await state.set_state(TradeState.setting_gridbot)

    elif get_trade_cache(user_id, 'grid_line') is None:
        _input = float(user_input)
        add_trade_cache(user_id, 'grid_line', _input)
        res_text = process_gridbot_trade_cache(user_id)
        await message.answer(res_text, reply_markup=two_way_button("Yes", "No"))
        await state.set_state(TradeState.setting_gridbot)

    else:
        if user_input.lower() == 'no':
            delete_trade_cache(user_id)
            await message.answer("Your Order has been successfully cancelled", reply_markup=home_button)
            return
        
      
# Grid Bot
def get_midmarket_price(client, market):
    orderbook = client.get_orderbook(market)
    best_bid = float(orderbook["bids"][0][0])
    best_ask = float(orderbook["asks"][0][0])
    midmarket_price = np.mean([best_bid, best_ask])
    return round(midmarket_price, 2)

async def start_gridbot(client, data):
    asyncio.get_event_loop().run_until_complete(aevo_gridbot(client, data))

async def aevo_gridbot(client, data):
    try:
        await client.open_connection()
        await client.subscribe_fills()

        # Data destructuring
        instrument_id = data['instrument_id']
        orderSize = data['order_size']
        gridSize = data['grid_size']
        girdLines = data['grid_line']
        instrument_name = data['instrument_name']
        midmarket_price = get_midmarket_price(client, instrument_name)

        async for msg in client.read_messages():
            message = json.loads(msg)
            if "data" in message and "success" in message["data"]:
                if message["data"]["success"] == True:
                    logger.info(
                        "🔌 Websocket connected at "
                        + str(pendulum.now())
                        + " to account "
                        + message["data"]["account"]
                    )
                    logger.info("🧑‍🍳 Starting Gridbot...")
                    for i in range(0, girdLines):
                        await client.create_order(
                            instrument_id,
                            True,
                            midmarket_price - (i * gridSize),
                            orderSize,
                        )
                        await asyncio.sleep(1)  # add a 1 second delay
                        await client.create_order(
                            instrument_id,
                            False,
                            midmarket_price + (i * gridSize),
                            orderSize,
                        )
                        await asyncio.sleep(1)  # add a 1 second delay
                else:
                    logger.info(message)
            elif "data" in message and "fill" in message["data"]:
                if message["data"]["fill"]["side"] == "buy":
                    logger.info("buy order filled")
                    logger.info("creating sell order")
                    await client.create_order(
                        instrument_id,
                        False,
                        float(message["data"]["fill"]["price"]) + gridSize,
                        orderSize,
                    )
                    logger.info(
                        "created new sell order at "
                        + str(float(message["data"]["fill"]["price"]) + gridSize)
                    )
                elif message["data"]["fill"]["side"] == "sell":
                    logger.info("sell order filled")
                    logger.info("creating buy order")
                    await client.create_order(
                        instrument_id,
                        True,
                        float(message["data"]["fill"]["price"]) - gridSize,
                        orderSize,
                    )
                    logger.info(
                        "created new buy order at "
                        + str(float(message["data"]["fill"]["price"]) - gridSize)
                    )
            else:
                logger.info(message)
    except Exception as e:
        logger.error(f"Connection closed unexpectedly: {e}")
        logger.info("Cancelling all orders...")
        await client.cancel_all_orders(instrument_id)
        logger.info("All orders cancelled.")
        logger.info("Websocket disconnected at " + str(pendulum.now()))
        logger.info("")
        logger.info("Attempting to reconnect at " + str(pendulum.now()) + "...")
        logger.info("")
        time.sleep(1)
        await aevo_gridbot()

