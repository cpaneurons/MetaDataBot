from aiogram import Bot, Dispatcher
from asyncio import get_event_loop

from bot.config import token
from bot.storage import storage

main_loop = get_event_loop()
bot = Bot(token=token)
dp = Dispatcher(bot=bot, loop=main_loop, storage=storage)

