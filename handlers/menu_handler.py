from aiogram.types import Message,  ReplyKeyboardRemove
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from database.db import get_user
from database.cache import add_message_entry, get_message_entry
from keyboards.menu import home_button, generate_menu
from Aevo_SDK.AlethieumAevoSDK import AevoClient

def validate_user(user_id: int):
    user = get_user(user_id)
    if user is None:
        return False
    return user

async def catch_all(message: Message):
    await message.answer("Please wait...", reply_markup=ReplyKeyboardRemove())

    user_id = message.from_user.id
    request = get_message_entry(user_id)
    if request is None:
        await message.answer("Please make a selection from the menu", reply_markup=home_button)
        return
    query = message.text.upper()

    user = get_user(user_id)
    if user is None:
        await message.answer("Please set up your account first", reply_markup=generate_menu())
        return
    
    aevo = AevoClient(**user)
    instrument = aevo.get_instrument(query)

    if 'error' in instrument:
        await message.answer(f'Instrument {query} query error\n{instrument["error"]}', reply_markup=home_button)
        return
    
    if request == "funding":
        funding = aevo.get_funding_rate(instrument['instrument_name'])
        if 'error' in funding:
            await message.answer(f'Funding rate for query resulted in an error\n{funding["error"]}', reply_markup=home_button)
            return
        
        from time import ctime
        
        next_epoch = int(funding['next_epoch']) / 10 ** 9
        await message.answer(f'Funding rate for {query} ({instrument["instrument_name"]}) is {funding["funding_rate"]}\nNext epoch is set at {ctime(next_epoch)}', reply_markup=home_button)

    elif request == "price":
        await message.answer(f'Price for {query} ({instrument["instrument_name"]}) is ${instrument["index_price"]}', reply_markup=home_button)

    else:
        await message.answer(f'Invalid query {query}', reply_markup=home_button)
        return
    
    add_message_entry(user_id, None)


async def get_alldata():
    url = "https://api.aevo.xyz/assets"
    headers = {"Accept": "application/json"}
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None