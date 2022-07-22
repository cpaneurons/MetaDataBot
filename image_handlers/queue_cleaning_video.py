from databases.database import FileDb


async def cleaning_file_db() -> bool:
    file_db = FileDb()
    file_db.delete_all()
    return True
