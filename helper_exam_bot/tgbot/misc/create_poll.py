import random
from typing import List
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiosqlite import Connection
from random import choice
from aiogram import Bot, Dispatcher
import aiosqlite

#                                             : Connection
from tgbot.states.state_answer import Answer


async def create_and_send_poll(bot: Bot, id : int,  db, state: FSMContext):
    cursor = await db.execute('SELECT COUNT(*) FROM all_exercises')
    count = await cursor.fetchone()
    random_index = random.randint(0, count[0] - 1)
    cursor = await db.execute('SELECT * FROM all_exercises LIMIT 1 OFFSET ?', (random_index,))
    row = await cursor.fetchone()

  #  answers = row[2]

    # for i in range(4):
    #     answers_list.append()
    # answer_0 = InlineKeyboardButton(answers.split()[0], callback_data='0')
    # answer_1 = InlineKeyboardButton(answers.split()[1], callback_data='1')
    # answer_2 = InlineKeyboardButton(answers.split()[2], callback_data='2')
    # answer_3 = InlineKeyboardButton(answers.split()[3], callback_data='3')
    #
    # keyboard4 = InlineKeyboardMarkup(row_width=2).add(answer_0, answer_1, answer_2, answer_3)
    # keyboard4 = keyboard4.insert(answer_2)
    # # keyboard4 = keyboard4.insert(answer_3)
    # print(answers, type(answers))
    #                                         reply_markup = keyboard4
    await bot.send_message(chat_id=id, text=row[1])
    await bot.send_poll(chat_id=id, question= ' ',
                                                options=row[2].split(), type="quiz",
                                                correct_option_id=row[3])






    right_index = row[3]
    # await Answer.answered.set()
    # await state.update_data(right_index=right_index)
    # await set_state(id, )
    # await state.set_state(Answer.answered)


async def set_state(user_id: int, state_value: str):
    bot = Bot.get_current()
    dp = Dispatcher.get_current()
    current_state = await dp.current_state(user=user_id)
    await current_state.set(state_value)



async def get_random_poll(db):
    ids = await (await db.execute('SELECT id_on_site FROM all_exercises')).fetchall()
    ids = [i[0] for i in ids]
    id = choice(ids)
    poll = await (await db.execute(f'SELECT * FROM all_exercises WHERE id_on_site = {id}')).fetchone()
    return poll







    #
    #
    # question = str( await db.execute(f"SELECT exercise FROM E_rus_4"))


    #
    # op_0 = await db.execute(f"SELECT op_0 FROM E_rus_4")
    #
    #
    # op_1 = await db.execute(f"SELECT op_1 FROM E_rus_4")
    #
    # op_2 = await db.execute(f"SELECT op_2 FROM E_rus_4")
    #
    # op_3 = await db.execute(f"SELECT op_3 FROM E_rus_4")

    # options=[]
    # options.append(op_0)
    # options.append(op_1)
    # options.append(op_2)
    # options.append(op_3)
    # print(options)
    #
    # correct_index =  (await db.execute(f"SELECT right_id FROM E_rus_4"))

    # '''
    # poll = get_random_poll(db)
    #  for option in poll[2]:
    #     # TODO создать клаву
    #     pass
    # await bot.send_message(chat_id=id, text=poll[1], reply_markup= exercise_poll)
    #
    #
    #
    # '''


    # await bot.send_poll(chat_id=id, question=question,
    #                         options=options, type="quiz",
    #                         correct_option_id=correct_index)


# async def test():
#     async with aiosqlite.connect(r'C:\Users\Tim89\PycharmProjects\Exam_helper_bot\db_of_exercises.db') as db:
#         print(await get_random_poll(db))
#
# import asyncio
# asyncio.run(test())

'''
a = ['a','b','c','d']

for i in range(0, len(a),3):
    print(a[i:i+3])


'''

