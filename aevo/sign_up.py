from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.blockchain import generate_eth_private_key, w3

cache = {}
async def sign_up(call: CallbackQuery, state: FSMContext):
    action = call.data.split(':')[1]
    user_id = call.from_user.id
    if action == "create":
        private_key = generate_eth_private_key()
        address = w3.eth.account.from_key(private_key).address
        return
    else:
        return


async def import_via_wallet():
    return