# -*- coding: utf-8 -*-
import shelve
# from SQLighter import SQLighter
from config import questionNum
from telebot import types


def get_question_num(chat_id):
    with shelve.open(questionNum) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def set_question_num(chat_id, i):
    with shelve.open(questionNum) as storage:
        storage[str(chat_id)] = i


def inc_question_num(chat_id):
    with shelve.open(questionNum) as storage:
        try:
            storage[str(chat_id)] = storage[str(chat_id)] + 1
        except KeyError:
            storage[str(chat_id)] = 1
            return None


def reset_question_num(chat_id):
    with shelve.open(questionNum) as storage:
        try:
            del storage[str(chat_id)]
        except KeyError:
            return None
