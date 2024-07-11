import aiosqlite as sq
from aiogram.types import CallbackQuery


async def upgrade_database(CQ: CallbackQuery, storage):
    async with sq.connect('exam_db.db') as db:
        # Создание курсора для выполнения запросов
        cursor = await db.cursor()

        # Создание таблицы
        await cursor.execute(
            'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, count TEXT)')

        # Добавление записей в таблицу
        await cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (
            CQ.from_user.id, str(CQ.from_user.first_name), storage["count"]))
##                                                      storage["grade"], storage["exam"],
        await cursor.close()

        # Сохранение изменений
        await db.commit()
