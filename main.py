from aiogram import executor
from bot.create_bot import dp
from bot.startup_bot import startup
from stop_fsm import register_stop_fsm_handler
from start_handlers.start_commands import register_handlers_start_commands
from image_handlers.exif_handlers import register_image_handlers


register_stop_fsm_handler(dp)
register_handlers_start_commands(dp)
register_image_handlers(dp)
if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=startup)
