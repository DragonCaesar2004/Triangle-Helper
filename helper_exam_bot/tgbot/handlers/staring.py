import random

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.database import upgrade_database
from tgbot.keyboards.inline import keyboard3
from tgbot.states.state_answer import Answer
from tgbot.states.state_starting import Starting


# grade exam count

async def starting(message: Message):


    await message.answer(text="Привет, это бот, который будет присылать тебе задания для подготовки к ЕГЭ по РУССКОМУ! "
                              "\n\nСколько раз в день хочешь получать заданий?  ", reply_markup=keyboard3)
#



    await Starting.daily_task_count.set()  # задали состояние. Теперь пользователь находится в этом состоянии
#
#
# # параметр state нужен для хранения данных в storage и для state.finish()
# async def choose_subject(CQ: CallbackQuery, state: FSMContext):
#     await CQ.answer()  # Чтобы не было значка часов при нажатии на кнопку
#     grade = CQ.data
#     await state.update_data(grade=grade)  # Закинули в Storage данные о классе обучения юзера
#     await CQ.bot.send_message(CQ.from_user.id, text="Теперь выберите предметы, к которым хотите подготовиться:",
#                               reply_markup=keyboard2)
#     await Starting.subject.set()
#
#
# async def choose_task_count(CQ: CallbackQuery, state: FSMContext):
#     await CQ.answer()  # Чтобы не было значка часов при нажатии на кнопку
#     exam = CQ.data
#     await state.update_data(exam=exam)
#     await CQ.bot.send_message(CQ.from_user.id, 'Сколько раз в день хочешь получать заданий?', reply_markup=keyboard3)
#     await Starting.daily_task_count.set()




async def end(CQ: CallbackQuery, state: FSMContext):
    await CQ.answer()  # Чтобы не было значка часов при нажатии на кнопку
    count = CQ.data
    await state.update_data(count=count)
    storage = await state.get_data()
    await upgrade_database(CQ, storage)
    await CQ.bot.send_message(chat_id=CQ.from_user.id, text='Отлично, в течение сегодняшнего дня бот пришлет Вам первое задание')
    await state.finish()



#async def create_and_send_poll(bot: Bot, id : int,  db, state: FSMContext):
    #    pass
        # cursor = await db.execute('SELECT COUNT(*) FROM all_exercises')
        # count = await cursor.fetchone()
        # random_index = random.randint(0, count[0] - 1)
        # cursor = await db.execute('SELECT * FROM all_exercises LIMIT 1 OFFSET ?', (random_index,))
        # row = await cursor.fetchone()
        #
        # answers = row[2]
        # answer_0 = InlineKeyboardButton(answers.split()[0], callback_data='0')
        # answer_1 = InlineKeyboardButton(answers.split()[1], callback_data='1')
        # answer_2 = InlineKeyboardButton(answers.split()[2], callback_data='2')
        # answer_3 = InlineKeyboardButton(answers.split()[3], callback_data='3')
        #
        # keyboard4 = InlineKeyboardMarkup(row_width=2).add(answer_0, answer_1,answer_2,answer_3)
        # # keyboard4 = keyboard4.insert(answer_2)
        # # # keyboard4 = keyboard4.insert(answer_3)
        # # print(answers, type(answers))
        #
        # await bot.send_message(chat_id=id,text = row[1], reply_markup=keyboard4)
        # right_index =  row[3]
        # # await Answer.answered.set()
        # #await state.update_data(right_index=right_index)
        # # await set_state(id, )
        # # await state.set_state(Answer.answered)







async def answer_got(CQ: CallbackQuery, state: FSMContext):
    await CQ.answer()  # Чтобы не было значка часов при нажатии на кнопку
    person_s_answer = CQ.data
    # await state.update_data(count=count)
    # storage = await state.get_data()
    # await upgrade_database(CQ, storage)

    right_id =await state.get_data()
    print(f'{right_id=}')



    if person_s_answer==right_id:
        await CQ.bot.send_message(chat_id=CQ.from_user.id, text='Отлично, в течение сегодняшнего дня бот пришлет Вам первое задание')
    await state.finish()


def register_starting(dp: Dispatcher):
    dp.register_message_handler(starting, commands=["start"])
    # dp.register_callback_query_handler(choose_subject, state=Starting.grade)
    # dp.register_callback_query_handler(choose_task_count, state=Starting.subject)
    dp.register_callback_query_handler(end, state=Starting.daily_task_count)
    dp.register_callback_query_handler(answer_got, state=Answer.answered)
