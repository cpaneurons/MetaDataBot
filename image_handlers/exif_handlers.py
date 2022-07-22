import traceback

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from bot.create_bot import dp, bot
from databases.database import VisuallyDB, FileDb
from image_handlers.keyboard_markup import keyboard_universalizer
from keyboard_stop_fsm import keyboard_stop_fsm
from image_handlers.fsm import FSMUniversalizer
from replacement_exif import replacement_exif_for_photo
from video_uniqueization import replacement_exif_for_video
from log.log import logger


# @dp.message_handler(Text(equals=['🌄 Уникализатор файлов']), commands=['unique'])
async def start_universalizer(message: Message):
    """Начало уникализации. Пользователю предоставляется выбор фото или видео"""
    if message.chat.type == 'private':
        await message.answer('Выберите один из предложенных вариантов ниже', reply_markup=keyboard_universalizer)


# @dp.callback_query_handler(Text(startswith='universalizer_'))
async def waiting_for_unique_file(callback: CallbackQuery):
    await callback.answer()
    visuall_db = VisuallyDB()
    mediafile = callback.data[14:]
    message = None

    if mediafile == 'photo':
        message = await callback.message.answer('Отправьте фото без сжатия (файлом)\n\n'
                                                '⚠️ Обратите внимание на то, что в Telegram есть '
                                                'ограничение на размер файла. '
                                                'Файл не должен превышать более 20 МБ⚠️',
                                                reply_markup=keyboard_stop_fsm)
        await FSMUniversalizer.photo.set()

    elif mediafile == 'video':
        message = await callback.message.answer('Отправьте видео (файлом)\n\n'
                                                '⚠️ Обратите внимание на то, что в Telegram есть'
                                                ' ограничение на размер файла. '
                                                'Файл не должен превышать более 20 МБ⚠️',
                                                reply_markup=keyboard_stop_fsm)
        await FSMUniversalizer.video.set()

    visuall_db.add_message_id(user_id=callback.from_user.id, message_id=message.message_id)


# @dp.message_handler(state=FSMUniversalizer.photo, content_types=['any'])
async def universalizer_photo(message: Message, state: FSMContext):
    if message.document:
        if message.document.mime_type[:5] == 'image':
            visual_db = VisuallyDB()
            file_info = await bot.get_file(message.document.file_id)
            try:
                # delete message
                message_id = visual_db.get_message_id(user_id=message.from_user.id)
                await bot.delete_message(message.chat.id, message_id=message_id)
                visual_db.delete_all_by_user_id(message.from_user.id)

                message_universalizer = await message.answer('Начинаю уникализацию...\n\n'
                                                             '🟩◻◻◻◻◻◻◻◻◻')

                await message.document.download()
                file_path = file_info.file_path
                new_path = await replacement_exif_for_photo(file_path, message_id=message_universalizer.message_id,
                                                            chat_id=message_universalizer.chat.id)
                with open(new_path, 'rb') as file_obj:
                    await bot.send_document(chat_id=message.chat.id, document=file_obj)

                await message_universalizer.edit_text('Готово!')
                await state.finish()
            except Exception:
                await message.answer('Возникла неизвестная ошибка. Попробуйте повторить уникализацию')
                traceback.print_exc()
                logger.warning(f'Во время выполнения отправки фото возникла ошибка \n{traceback.print_exc()}')
            finally:
                pass
                # Удаление файла
                # time.sleep(400)
                # if os.path.isfile(file_info.file_path):
                #     os.remove(file_info.file_path)
                #
                # if os.path.isfile(new_path):
                #     os.remove(new_path)
        else:
            await message.answer('Необходимо отправлять файл - фотографию')
    else:
        await message.answer('Ожидалось фото(файл). Попробуйте еще раз или приостановите операцию при помощи команды '
                             '"/stop"')


# @dp.message_handler(state=FSMUniversalizer.video, content_types=['any'])
async def universalizer_video(message: Message, state: FSMContext):
    if message.document:
        if message.document.mime_type[:5] == 'video':
            await state.finish()
            visual_db = VisuallyDB()
            file_db = FileDb()
            file_info = await bot.get_file(message.document.file_id)
            try:
                # delete message
                message_id = visual_db.get_message_id(user_id=message.from_user.id)
                await bot.delete_message(message.chat.id, message_id=message_id)
                visual_db.delete_all_by_user_id(message.from_user.id)

                message_universalizer = await message.answer('Начинаю уникализацию...\n\n'
                                                             '🟩◻◻◻◻◻◻◻◻◻')

                await message.document.download()
                file_path = file_info.file_path
                new_path = await replacement_exif_for_video(file_path, message_id=message_universalizer.message_id,
                                                            chat_id=message_universalizer.chat.id,
                                                            user_id=message.from_user.id)
                with open(new_path, 'rb') as file_obj:
                    await bot.send_video(chat_id=message.chat.id, video=file_obj)

                await message_universalizer.edit_text('Готово!')
            except Exception:
                await message.answer('Возникла неизвестная ошибка. Попробуйте повторить уникализацию')
                traceback.print_exc()
                logger.warning(f'Во время выполнения отправки фото возникла ошибка \n{traceback.print_exc()}')
            finally:
                if file_db.file_exists(user_id=message.from_user.id):
                    file_db.delete_all_by_user_id(user_id=message.from_user.id)
                # Удаление файла
                # time.sleep(400)
                # if os.path.isfile(file_info.file_path):
                #     os.remove(file_info.file_path)
                #
                # if os.path.isfile(new_path):
                #     os.remove(new_path)
        else:
            await message.answer('Необходимо отправлять видео')
    else:
        await message.answer('Ожидалось видео. Попробуйте еще раз или приостановите операцию при помощи команды '
                             '"/stop"')


def register_image_handlers(dp: dp):
    dp.register_message_handler(start_universalizer, Text(equals=['🌄 Уникализатор файлов 📷', 'Уникализировать']))
    dp.register_message_handler(start_universalizer, commands=['universalizer', 'us'])
    dp.register_callback_query_handler(waiting_for_unique_file, Text(startswith='universalizer_'), state=None)
    dp.register_message_handler(universalizer_photo, state=FSMUniversalizer.photo, content_types=['any'])
    dp.register_message_handler(universalizer_video, state=FSMUniversalizer.video, content_types=['any'])
