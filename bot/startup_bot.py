import asyncio
import aioschedule
from image_handlers.queue_cleaning_video import cleaning_file_db
from delete_dir import delete_document_dir


async def scheduler():
    aioschedule.every(20).minutes.do(cleaning_file_db)  # каждые 20 минут чистим БД
    aioschedule.every().day.at('02:00').do(delete_document_dir)
    while 1:
        await aioschedule.run_pending()
        await asyncio.sleep(3)


async def startup(_):
    asyncio.create_task(scheduler())
    print('Bot started')
