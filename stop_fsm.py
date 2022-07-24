from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.create_bot import dp, bot
from start_handlers.keyboard_markup import keyboard_menu_start
from databases.database import VisuallyDB


# @dp.message_handler(commands='stop', state='*')
# @dp.message_handler(Text(equals=['stop', 'стоп'], ignore_case=True), state='*')
async def stop_fsm(message: [Message, CallbackQuery], state: FSMContext):
    message_db = VisuallyDB()
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    chat_id = None
    try:  # callback
        chat_id = message.message.chat.id
        await message.answer()
        await message.message.answer('Операция успешно остановлена')
    except Exception:  # message
        chat_id = message.chat.id
        await message.answer('Операция успешно остановлена', reply_markup=keyboard_menu_start)

    message_id = message_db.get_message_id(user_id=message.from_user.id)
    message_db.delete_all_by_user_id(user_id=message.from_user.id)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


def register_stop_fsm_handler(dp: dp):
    dp.register_message_handler(stop_fsm, commands='stop', state='*')
    dp.register_message_handler(stop_fsm, Text(equals=['stop', 'стоп', '❌Отмена'], ignore_case=True), state='*')
    dp.register_callback_query_handler(stop_fsm, Text(equals='stop_fsm', ignore_case=True), state='*')
