from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard_menu_start = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
uniqueization_button = KeyboardButton('🌄 Уникализатор файлов 📷')
keyboard_menu_start.insert(uniqueization_button)
