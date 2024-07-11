from datetime import datetime
import aiosqlite as sq
import pytz
from aiogram import Bot

from tgbot.misc.create_poll import create_and_send_poll
from tgbot.misc.read_column import column_of_counts
from tgbot.states.state_answer import Answer


async def send_my_poll(bot: Bot):
    # создание объекта часового пояса для Москвы
    tz = pytz.timezone('Europe/Moscow')
    # получение текущей даты и времени в Москве
    now = datetime.now(tz)
    # вывод даты и времени в формате 'YYYY-MM-DD HH:MM:SS'
    hours = now.strftime('%Y-%m-%d %H:%M:%S')[11:13]

    # govno_code

    # TODO CREATING POLL


    # *говнокод
    db =await sq.connect('exam_db.db')

    cursor = db.cursor()

    async for id, count in column_of_counts("exam_db.db", "users", "user_id", "count"):
        if count == '6':
            await create_and_send_poll(bot,id, db, Answer.answered)
            # отправляем в любом случае
            continue


        elif count == '5' and hours[11:13] != '09':
            # отправляем в кроме 09.35
            await create_and_send_poll(bot,id, db,Answer.answered)
            continue


        elif count == '4' and hours[11:13] != '13':
            # отправляем в кроме 09.35 и 13.35
            await create_and_send_poll(bot,id, db,Answer.answered)
            continue


        elif count == '3' and hours[11:13] != '15':
            # отправляем в кроме 09.35 , 13.35 и 15.35
            await create_and_send_poll(bot,id, db,Answer.answered)
            continue


        elif count == '2' and hours[11:13] != '19':
            # отправляем в кроме 09.35, 13.35 , 15.35 и 19.35
            await create_and_send_poll(bot,id, db,Answer.answered)
            continue


        elif count == '1' and hours[11:13] != '11':
            # отправляем в 17.35
            await create_and_send_poll(bot,id, db,Answer.answered)
            continue

    cursor.close()
    await db.close()


















    # GPT ПРЕДЛОЖИЛ
    # forbidden_hours = {'5': '09', '4': '13', '3': '15', '2': '19', '1': '11'}
    # for id, count in await column_of_counts("exam_db.db", "users", "user_id", "count"):
    #     if count == '6':
    #         pass
    #     elif count == '1' and hours[11:13] == '17':
    #         pass
    #     elif hours[11:13] != forbidden_hours.get(count, ''):
    #         pass
