# -*- coding: utf-8 -*-
from telebot import TeleBot
from telebot import types
from threading import Thread
from os import remove

import messages as msg
from config import *
from functions import *
import keyboard as kb
from db import DB

bot = TeleBot(token, skip_pending=True, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def main_message(message):
    text = message.text
    user_id = message.chat.id
    print(message.from_user.first_name, ':' , user_id, ':', text)
    db = DB()
    db.insert_user(user_id)
    db.close()
    if text == '/start':
        bot.send_message(user_id, msg.start, reply_markup=kb.start(user_id in admins))
    elif text == 'Админка' and user_id in admins:
        bot.send_message(user_id, msg.start_admin, reply_markup=kb.admin())
    else:
        db = DB()
        db.set_user_values(user_id)
        db.close()
        bot.send_photo(user_id, photo=open('tri.png', 'rb'), caption=msg.caption)
        send_values(user_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    data = call.data
    if data != 'restart':
        bot.delete_message(user_id, call.message.id)

    if data == 'statistic':
        db = DB()
        users = db.extract_users()
        db.close()
        bot.send_message(user_id, msg.statistic.format(len(users)), reply_markup=kb.cancel())
    elif data == 'cancel':
        bot.send_message(user_id, msg.start_admin, reply_markup=kb.admin())
    elif data == 'mailing':
        m = bot.send_message(user_id, msg.mailing)
        bot.register_next_step_handler(m, mailing_hand)
    elif data == 'start_mailing':
        db = DB()
        text = db.extract_data()
        db.close()
        Thread(target=mailing, args=[text]).start()
        bot.send_message(user_id,msg.mailing_started)
    elif data == 'restart':
        db = DB()
        db.set_user_values(user_id)
        db.close()
        bot.send_photo(user_id, photo=open('tri.png', 'rb'), caption=msg.caption)
        send_values(user_id)
        #bot.register_next_step_handler(m, hand)
    elif data == 'calculate':
        try:
            db = DB()
            data = db.extract_values(user_id)
            db.close()
            dict = get_dict()
            value_types = list(value_names.keys())
            for i, value in enumerate(data[1:], start=0):
                value_type = value_types[i]
                dict[value_type] = value

            dict = find_all(dict)
            user_values = tuple(dict.values())
            photo = get_photo(dict, user_id)
            with open(photo, 'rb') as file:
                bot.send_photo(user_id, photo=file, caption=msg.result % user_values, reply_markup=kb.restart())
            if not 'unknown' in photo: remove(photo)
            #bot.send_message(user_id, msg.result % user_values, reply_markup=kb.restart())
        except Exception as e:
            bot.send_message(user_id, msg.error)
            db = DB()
            db.set_user_values(user_id)
            db.close()

    elif 'value' in data:
        _, user_id, value = data.split(':')
        db = DB()
        db.insert_user_last_data(user_id, value)
        db.close()
        m = bot.send_message(user_id, msg.except_value.format(value_names[value]))
        bot.register_next_step_handler(m, except_value_hand)

def except_value_hand(message):
    user_id = message.chat.id
    text = message.text
    message_id = message.message_id
    bot.delete_message(user_id, message_id)
    bot.delete_message(user_id, message_id - 1)
    db = DB()
    db.update_value(user_id, text)
    db.close()
    send_values(user_id)


def send_values(user_id):
    db = DB()
    data = db.extract_values(user_id)
    db.close()
    bot.send_message(user_id, msg.instruction, reply_markup=kb.values(data, user_id))



def mailing(text):
    db = DB()
    users = db.extract_users()
    db.close()
    sended = 0
    dissended = 0
    for user in users:
        try:
            bot.send_message(user, text)
            sended += 1
        except:
            db = DB()
            db.delete_user(user)
            db.close()
            dissended += 1
    for admin in admins:
        bot.send_message(admin, msg.mailing_ended.format(sended, dissended))

def mailing_hand(message):
    user_id = message.chat.id
    text = message.text
    db = DB()
    db.insert_data(text)
    db.close()
    bot.send_message(user_id, msg.start_mailing.format(text), reply_markup=kb.mailing())

y3='''
def hand(message):
    user_id = message.chat.id
    text = message.text
    try:
        dict = {}
        for index in values.values():
            dict.update({index: None})
        for i in text.split('\n'):
            index, value = i.split(' ')
            value = value.replace(',', '.')
            dict[values[index]] = float(value)
        dict = find_all(dict)
        user_values = tuple(dict.values())
        photo = get_photo(dict, user_id)
        with open(photo, 'rb') as file:
            bot.send_photo(user_id, photo=file, caption=msg.result % user_values, reply_markup=kb.restart())
        if not 'unknown' in photo: remove(photo)
        # bot.send_message(user_id, msg.result % user_values, reply_markup=kb.restart())
    except Exception as e:
        #raise e
        bot.send_message(user_id, msg.error)
'''

bot.polling(none_stop=True)









