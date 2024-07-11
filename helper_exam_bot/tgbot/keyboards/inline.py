from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button9 = InlineKeyboardButton(text="ОГЭ", callback_data="9")
button11 = InlineKeyboardButton(text="ЕГЭ", callback_data="11")
keyboard1 = InlineKeyboardMarkup().add(button9, button11)

button_m = InlineKeyboardButton(text="Математика", callback_data="math")
button_r = InlineKeyboardButton(text="Русский", callback_data="rus")
button_mr = InlineKeyboardButton(text="Мат + Русс", callback_data="math_and_rus")
keyboard2 = InlineKeyboardMarkup().add(button_m, button_r, button_mr)

button_1 = InlineKeyboardButton('1', callback_data='1')
button_2 = InlineKeyboardButton('2', callback_data='2')
button_3 = InlineKeyboardButton('3', callback_data='3')
button_4 = InlineKeyboardButton('4', callback_data='4')
button_5 = InlineKeyboardButton('5', callback_data='5')
button_6 = InlineKeyboardButton('6', callback_data='6')
keyboard3 = InlineKeyboardMarkup().add(button_1, button_2, button_3, button_4, button_5, button_6)









#exercise_poll = InlineKeyboardButton().add()
