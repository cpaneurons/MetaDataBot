from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_universalizer = InlineKeyboardMarkup(row_width=2)
photo_universalizer = InlineKeyboardButton('Уникализацировать фото', callback_data='universalizer_photo')
video_universalizer = InlineKeyboardButton('Уникализацировать видео', callback_data='universalizer_video')
keyboard_universalizer.insert(photo_universalizer).insert(video_universalizer)
