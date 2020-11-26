# -*- coding: utf-8 -*-
import shelve
# from SQLighter import SQLighter
from config import userSum
from telebot import types


def get_user_sum(chat_id):
    with shelve.open(userSum) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def set_user_sum(chat_id, i):
    with shelve.open(userSum) as storage:
        try:
            storage[str(chat_id)] = storage[str(chat_id)] + i
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            storage[str(chat_id)] = i


def reset_user_sum(chat_id):
    with shelve.open(userSum) as storage:
        try:
            del storage[str(chat_id)]
        except KeyError:
            return None
