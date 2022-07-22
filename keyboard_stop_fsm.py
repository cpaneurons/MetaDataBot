from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_stop_fsm = InlineKeyboardMarkup(row_width=1)
stop_fsm_button = InlineKeyboardButton(text='Стоп', callback_data='stop_fsm')
keyboard_stop_fsm.insert(stop_fsm_button)
