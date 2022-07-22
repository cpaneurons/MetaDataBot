import asyncio
import ffmpeg
import random
import hashlib

import moviepy.editor as mp
from asynccpu import ProcessTaskPoolExecutor
from asyncffmpeg import FFmpegCoroutineFactory, StreamSpec

from databases.database import FileDb
from bot.create_bot import bot


def get_name_video() -> str:
    """Рандомная генерация имени с последующим хешированием"""
    alphabet = 'qwertyuiopasdfghjklzxcvbnm'
    digits = '123456789'

    num_digits = len(digits)
    num_alphabet = len(alphabet)

    name = ''

    for digit in digits:
        num = random.randint(0, num_digits - 1)
        name += digits[num] + digit

    for abc in alphabet:
        num = random.randint(0, num_alphabet - 1)
        name += alphabet[num] + abc

    name = bytes(name, encoding='utf-8')

    hash_name = hashlib.md5(name)

    finish_name = r'documents/' + hash_name.hexdigest() + '.mp4'
    return finish_name


async def create_stream_spec_filter() -> StreamSpec:
    file_db = FileDb()
    info = file_db.get_all()[0]
    print(info)
    height = info[-1]
    width = info[3]
    file_path = info[1]
    new_file_path = info[2]
    stream = ffmpeg.input(file_path)
    stream = ffmpeg.filter(stream, "scale", width, height)
    stream = ffmpeg.filter(stream, "colorcorrect", 0.001)
    # stream = ffmpeg.filter(stream, "avgblur", 1)
    stream = ffmpeg.filter(stream, 'eq', contrast=0.9, brightness=0.01, saturation=1.1, gamma=0.9)
    return ffmpeg.output(stream, new_file_path)


async def replacement_exif_for_video(file_path, message_id, chat_id, user_id):
    file_db = FileDb()
    while True:
        if file_db.get_all():
            await bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Вы находитесь в очереди\n\n'
                                                                                     '🟩🟩◻◻◻◻◻◻◻◻')
            await asyncio.sleep(20)
            num = random.randint(1, 2)
            if num == 1:
                await bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Вы все ещё в очереди\n\n'
                                                                                         '🟩🟩◻◻◻◻◻◻◻◻')
            if num == 2:
                await bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Мы обязательно справимся с '
                                                                                         'нагрузкой!\n\n'
                                                                                         '🟩🟩◻◻◻◻◻◻◻◻')
        else:
            break

    new_file_path = get_name_video()
    clip = (mp.VideoFileClip(file_path))
    clip1 = clip.subclip(0, 10)
    width = clip1.w - 2
    height = clip.h - 2
    await bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Изменяем данные...\n\n'
                                                                             '🟩🟩🟩◻◻◻◻◻◻◻')
    # # Изменение размера, контрастности, светимости, оттенков и цветовой гаммы
    # finish_clip = clip.fx(vfx.resize, height=height, width=width).fx(vfx.lum_contrast, 0.1, 0.1, 127) \
    #     .fx(vfx.colorx, 1.01).fx(vfx.gamma_corr, 1)
    #
    # finish_clip.write_videofile(name)

    file_db.add_data(user_id=user_id, file_path=file_path, new_file_path=new_file_path, width_file=width,
                     height_file=height)

    await bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Чуть-чуть яркости...\n\n'
                                                                             '🟩🟩🟩🟩🟩◻◻◻◻◻')

    ffmpeg_coroutine = FFmpegCoroutineFactory.create()

    await bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Вносим изменения в видео...\n'
                                                                             'Иногда это может занимать '
                                                                             'несколько минут\n\n'
                                                                             '🟩🟩🟩🟩🟩🟩🟩🟩◻◻')

    with ProcessTaskPoolExecutor(max_workers=3, cancel_tasks_when_shutdown=True) as executor:
        awaitables = (
            executor.create_process_task(ffmpeg_coroutine.execute, create_stream_spec)
            for create_stream_spec in [create_stream_spec_filter]
        )
        await asyncio.gather(*awaitables)

    if file_db.file_exists(user_id=user_id):
        file_db.delete_all_by_user_id(user_id=user_id)

    await bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Готово!\nОтправляем видео...\n\n'
                                                                             '🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩')

    return new_file_path
