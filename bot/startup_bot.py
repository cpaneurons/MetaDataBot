import asyncio
import aioschedule
from image_handlers.queue_cleaning_video import cleaning_file_db


async def scheduler():
    aioschedule.every(20).minutes.do(cleaning_file_db)  # каждые 20 минут чистим БД
    while 1:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def startup(_):
    asyncio.create_task(scheduler())
    print('Bot started')
