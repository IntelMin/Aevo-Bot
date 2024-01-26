from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, URLInputFile, ForceReply
import aiohttp
from keyboards.menu import key_menu
# Global session for aiohttp to improve efficiency.
aiohttp_session = aiohttp.ClientSession()


wallet1 = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/wallet-1.png"
wallet2 = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/wallet-2.png"
wallet3 = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/wallet-3.png"
address = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/wallet-4.png"
info1 = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/info-1.png"
info2 = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/info-2.png"
info_sign = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/info-sign.png"
info_sign_key = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/info-sign-key.png"
info_api = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/info-api.png"
info_api_key = "https://vbaewhdathwocxihuyfe.supabase.co/storage/v1/object/public/guide/info-api-key.png"

async def get_info_callback(callback: CallbackQuery, state: FSMContext):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(wallet1) as response:
                if response.status == 200:
                    photo_guide_1 = URLInputFile(wallet1)
                    photo_guide_2 = URLInputFile(wallet2)
                    photo_guide_3 = URLInputFile(wallet3)
                    photo_set_address = URLInputFile(address)
                    await callback.message.answer("First of all, you have to join here: https://www.aevo.xyz\n" 
                                                  "In this step, you can set wallet address")
                    await callback.message.answer_photo(
                        photo=photo_guide_1,
                        caption="Please click button 'launch Exchange' in the upper right corner.\n",
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_guide_2,
                        caption="Please click button 'Connect Wallet' in the upper right corner.\n",
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_guide_3,
                        caption="If Wallet is not installed, install Wallet.\n"
                            "You can install Matamask or Coinbase extension.",
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_set_address,
                        reply_markup=ForceReply(selective=True)
                    )
                    keyboard = key_menu() 
                    await callback.message.answer(
                        text="Please Select",
                        parse_mode='Markdown',
                        reply_markup=keyboard
                    )
                else:
                    await callback.message.answer(f"Failed to fetch the image. HTTP Status: {response.status}")
    except Exception as e:
        await callback.message.answer(f"An error occurred while fetching the image: {e}")

    await state.set_state(None)  

async def get_signinKey_callback(callback: CallbackQuery, state: FSMContext):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(wallet1) as response:
                if response.status == 200:
                    photo_guide_info1 = URLInputFile(info1)
                    photo_guide_info2 = URLInputFile(info2)
                    photo_guide_info_sign = URLInputFile(info_sign)
                    photo_get_signinkey = URLInputFile(info_sign_key)
                    await callback.message.answer_photo(
                        photo=photo_guide_info1,
                        caption="You can simply access the API at the following URL: https://api-docs.aevo.xyz/reference/overview.\n",
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_guide_info2,
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_guide_info_sign,
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_get_signinkey,
                        reply_markup=ForceReply(selective=True)
                    )
                    keyboard = key_menu() 
                    await callback.message.answer(
                        text="Please Select",
                        parse_mode='Markdown',
                        reply_markup=keyboard
                    )
                else:
                    await callback.message.answer(f"Failed to fetch the image. HTTP Status: {response.status}")
    except Exception as e:
        await callback.message.answer(f"An error occurred while fetching the image: {e}")

    await state.set_state(None)  

async def get_api_callback(callback: CallbackQuery, state: FSMContext):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(wallet1) as response:
                if response.status == 200:
                    photo_guide_info1 = URLInputFile(info1)
                    photo_guide_info2 = URLInputFile(info2)
                    photo_guide_info_api = URLInputFile(info_api)
                    photo_get_api = URLInputFile(info_api_key)
                    await callback.message.answer_photo(
                        photo=photo_guide_info1,
                        caption="You can simply access the API at the following URL: https://api-docs.aevo.xyz/reference/overview.\n",
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_guide_info2,
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_guide_info_api,
                        reply_markup=ForceReply(selective=True)
                    )
                    await callback.message.answer_photo(
                        photo=photo_get_api,
                        reply_markup=ForceReply(selective=True)
                    )
                    keyboard = key_menu() 
                    await callback.message.answer(
                        text="Please Select",
                        parse_mode='Markdown',
                        reply_markup=keyboard
                    )
                else:
                    await callback.message.answer(f"Failed to fetch the image. HTTP Status: {response.status}")
    except Exception as e:
        await callback.message.answer(f"An error occurred while fetching the image: {e}")

    await state.set_state(None)  