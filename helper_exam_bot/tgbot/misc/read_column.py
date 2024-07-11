import aiosqlite


async def column_of_counts(db_file, table_name, user_id, count):
    async with aiosqlite.connect(db_file) as db:
        cursor = await db.execute(f"SELECT {user_id},{count} FROM {table_name}")
        async for row in cursor:
            yield (row[0], row[1])
