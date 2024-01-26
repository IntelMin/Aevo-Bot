import asyncio
from aiogram import Bot, Dispatcher

from utils.logger import Logger
from utils.config import BOT_TOKEN, BOT_NAME
from handlers import common

log = Logger(BOT_NAME)
log.debug("Bot is loading")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    
    log.debug("Bot initializing.")
    
    await common.set_bot_commands(bot)
    
    dp.include_routers(
        common.router,
    )
    
    log.debug("Bot commands and routers loaded.")
    
    # initalize_queue()
    
    # log.debug("Transaction queue initalized.")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())