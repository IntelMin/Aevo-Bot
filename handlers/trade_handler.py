from aiogram.types import Message,  ReplyKeyboardRemove
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from database.db import get_user, get_cache_entry, add_cache_entry
from keyboards.menu import home_button, generate_menu
from Aevo_SDK.AlethieumAevoSDK import AevoClient


