from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard_stop_fsm = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
stop_fsm_button = KeyboardButton(text='❌Отмена')
keyboard_stop_fsm.insert(stop_fsm_button)
