# -*- coding: utf-8 -*-
import shelve
# from SQLighter import SQLighter
from config import shelve_name


def generate_markup(i):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in range(i):
        button = types.KeyboardButton(text=item + 1)
        markup.add(button)
    return markup


# def count_rows():
#     """
#     Данный метод считает общее количество строк в базе данных и сохраняет в хранилище.
#     Потом из этого количества будем выбирать музыку.
#     """
#     db = SQLighter(database_name)
#     rowsnum = db.count_rows()
#     with shelve.open(shelve_name) as storage:
#         storage['rows_count'] = rowsnum
#
#
# def get_rows_count():
#     """
#     Получает из хранилища количество строк в БД
#     :return: (int) Число строк
#     """
#     with shelve.open(shelve_name) as storage:
#         rowsnum = storage['rows_count']
#     return rowsnum
#
#
# def set_user_game(chat_id, i):
#     """
#     Записываем юзера в игроки и запоминаем, что он должен ответить.
#     :param i:
#     :param chat_id: id юзера
#     :param estimated_answer: правильный ответ (из БД)
#     """
#     with shelve.open(shelve_name) as storage:
#         storage[str(chat_id)] = i
#
#
# def finish_user_game(chat_id):
#     """
#     Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
#     :param chat_id: id юзера
#     """
#     with shelve.open(shelve_name) as storage:
#         del storage[str(chat_id)]
#
#
# def get_answer_for_user(chat_id):
#     """
#     Получаем правильный ответ для текущего юзера.
#     В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
#     :param chat_id: id юзера
#     :return: (str) Правильный ответ / None
#     """
#     with shelve.open(shelve_name) as storage:
#         try:
#             answer = storage[str(chat_id)]
#             return answer
#         # Если человек не играет, ничего не возвращаем
#         except KeyError:
#             return None


from telebot import types
