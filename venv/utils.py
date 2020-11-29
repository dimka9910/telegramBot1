# -*- coding: utf-8 -*-
import shelve
from telebot import types
from config import shelve_name


# генерирует раскладку экранной клавиатуры
def generate_markup(i):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in range(i):
        button = types.KeyboardButton(text=item + 1)  # заполняем просто цифрами от 1 до i
        markup.add(button)
    return markup
