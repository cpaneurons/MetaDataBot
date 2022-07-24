import traceback

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from bot.create_bot import dp, bot
from databases.database import VisuallyDB, FileDb
from keyboard_stop_fsm import keyboard_stop_fsm
from image_handlers.fsm import FSMUniversalizer
from replacement_exif import replacement_exif_for_photo
from video_uniqueization import replacement_exif_for_video
from log.log import logger


# @dp.message_handler(Text(equals=['🌄 Уникализатор файлов']), commands=['unique'])
async def start_universalizer(message: Message):
    """Начало уникализации. Пользователю предоставляется выбор фото или видео"""
    if message.chat.type == 'private':
        visuall_db = VisuallyDB()
        message_bot = await message.answer('Отправьте фото без сжатия (файлом) или же видео (файлом)\n\n'
                                           '⚠️ Обратите внимание на то, что в Telegram есть ограничение на размер файла'
                                           ' Файл не должен превышать более 20 МБ⚠️\n\n'
                                           'Если хотите остановить операцию, то воспользуйтесь кнопкой ниже',
                                           reply_markup=keyboard_stop_fsm)
        await FSMUniversalizer.file.set()
        visuall_db.add_message_id(user_id=message.from_user.id, message_id=message_bot.message_id)


# @dp.message_handler(state=FSMUniversalizer.file, content_types=['any'])
async def universalizer_file(message: Message, state: FSMContext):
    print(message)
    if message.video:
        await state.finish()
        visual_db = VisuallyDB()
        file_db = FileDb()
        file_info = await bot.get_file(message.video.file_id)
        try:
            # delete message
            message_id = visual_db.get_message_id(user_id=message.from_user.id)
            await bot.delete_message(message.chat.id, message_id=message_id)
            visual_db.delete_all_by_user_id(message.from_user.id)

            message_universalizer = await message.answer('Начинаю уникализацию...\n\n'
                                                         '🟩◻◻◻◻◻◻◻◻◻')

            await message.video.download()
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
            await state.finish()
            if file_db.file_exists(user_id=message.from_user.id):
                file_db.delete_all_by_user_id(user_id=message.from_user.id)

    elif message.document:
        # Уникализация фото файла
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
            except Exception:
                await message.answer('Возникла неизвестная ошибка. Попробуйте повторить уникализацию')
                traceback.print_exc()
                logger.warning(f'Во время выполнения отправки фото возникла ошибка \n{traceback.print_exc()}')
            finally:
                await state.finish()

        # Уникализация видео файла
        elif message.document.mime_type[:5] == 'video':
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
                await state.finish()
                if file_db.file_exists(user_id=message.from_user.id):
                    file_db.delete_all_by_user_id(user_id=message.from_user.id)
        else:
            await message.answer('Необходимо отправлять файл - фотографию или же видео')
    else:
        await message.answer('Ожидалось фото(файл) или же видео (файл)'
                             ' Попробуйте еще раз или приостановите операцию при помощи команды '
                             '"/stop"')


def register_image_handlers(dp: dp):
    dp.register_message_handler(start_universalizer, Text(equals=['🌄 Уникализатор файлов 📷', 'Уникализировать']))
    dp.register_message_handler(start_universalizer, commands=['universalizer', 'us'])
    dp.register_message_handler(universalizer_file, state=FSMUniversalizer.file, content_types=['any'])
