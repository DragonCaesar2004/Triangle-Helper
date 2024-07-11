from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,InlineKeyboardButton
from config import value_names

def start(is_admin):
    keyboard =  ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add('Начать')
    if is_admin:
        keyboard.add('Админка')
    return keyboard

def admin():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text='Рассылка', callback_data='mailing'))
    keyboard.row(InlineKeyboardButton(text='Статистика', callback_data='statistic'))
    return keyboard

def mailing():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text='Начать рассылку', callback_data='start_mailing'))
    keyboard.row(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return keyboard

def cancel():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='cancel'))
    return keyboard

def restart():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text='Начать заново', callback_data='restart'))
    return keyboard

def values(data, user_id):
    keyboard = InlineKeyboardMarkup()
    value_types = list(value_names.keys())
    value_type_names = list(value_names.values())
    for i, value in enumerate(data[1:], start=0):
        value_type = value_types[i]
        value_name = value_type_names[i]
        if not value: value = 'не указано'
        keyboard.row(InlineKeyboardButton(text=f'{value_name}: {value}', callback_data=f'value:{user_id}:{value_type}'))
    keyboard.row(InlineKeyboardButton(text='Рассчитать значения', callback_data='calculate'))
    return keyboard