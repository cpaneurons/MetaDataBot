from aiogram.types import Message

from bot.create_bot import dp
from start_handlers.keyboard_markup import keyboard_menu_start


# @dp.message_handler(commands='start')
async def command_start(message: Message):
    if message.chat.type == 'private':
        await message.answer('👋 Привет! Я бот-уникализатор, '
                             'могу уникализировать видео и фотографии для вас без потери качества\n\n'
                             '✴ К сожалению, ограничения телеграма не дают заливать файлы больше 20 мегабайт,'
                             ' обращайте на это внимание при работе\n\n'
                             '✴ После загрузки видео или фото вы получите уникализированную копию вашего файла\n\n'
                             '✴ На данный момент я работаю полностью бесплатно, Вам доступен полный мой функционал\n\n'
                             '✴ Вы можете использовать команду "/universalizer" для вызова уникализации или же для '
                             'простоты "/us"\n\n'
                             '✨Желаем приятной работы✨',
                             reply_markup=keyboard_menu_start)


def register_handlers_start_commands(dp: dp):
    dp.register_message_handler(command_start, commands='start')
