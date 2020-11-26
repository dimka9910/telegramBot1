# -*- coding: utf-8 -*-
import shelve
# from SQLighter import SQLighter
from config import testNum
from telebot import types


def get_test_num(chat_id):
    with shelve.open(testNum) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def set_test_num(chat_id, i):
    with shelve.open(testNum) as storage:
        storage[str(chat_id)] = i


def reset_test_num(chat_id):
    with shelve.open(testNum) as storage:
        try:
            del storage[str(chat_id)]
        except KeyError:
            return None
