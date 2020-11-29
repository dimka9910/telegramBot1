# -*- coding: utf-8 -*-
import config
import telebot
import random
import time
import utils
import testNumFile
import userSumFile
import questionNumFile
from telebot import types
from SqlLighter import SQLighter

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    reset(message)
    bot.send_message(message.chat.id, 'Привет! Введи номер теста который хочешь пройти')
    testNumFile.set_test_num(message.chat.id, 0)
    db_worker = SQLighter(config.database_name)
    text = ''
    i = 1
    for row in (db_worker.select_all_tests()):
        text += str(i) + ") " + str(row[0]) + '\n'
        i += 1
    bot.send_message(message.chat.id, text)
    db_worker.close()


@bot.message_handler(commands=['reset'])
def reset(message):
    testNumFile.reset_test_num(message.chat.id)
    questionNumFile.reset_question_num(message.chat.id)
    userSumFile.reset_user_sum(message.chat.id)
    # check_answer(message)


def test_selector(message):
    db_worker = SQLighter(config.database_name)
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Введи пожалуйста номер теста :)")
        db_worker.close()
        return
    if int(message.text) > db_worker.test_len():
        bot.send_message(message.chat.id, "Такого номера нет в списке :(")
        db_worker.close()
        return
    i = 0
    for row in (db_worker.select_test_code()):
        i += 1
        if i == int(message.text):
            testNumFile.set_test_num(message.chat.id, int(row[0]))
            questionNumFile.set_question_num(message.chat.id, 1)
            db_worker.close()
            check_answer(message)
            return

def question_handler(message):
    if message.text is None:
        return

    if message.text == '/reset' or message.text == '/start':
        types.ReplyKeyboardRemove()
        start(message)
        return

    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Введите число с клавиатуры")
        check_answer(message)
        return

    db_worker = SQLighter(config.database_name)
    t_num = testNumFile.get_test_num(message.chat.id)
    q_num = questionNumFile.get_question_num(message.chat.id)

    i = 0
    k = '{}'.format(db_worker.select_question(t_num, q_num)[5])
    list_keys = []
    for item in k.split(','):
        i += 1
        list_keys.append(item)

    db_worker.close()

    if int(message.text) < 1 or int(message.text) > i:
        bot.send_message(message.chat.id, "Введите число с клавиатуры")
        check_answer(message)
        return

    i = 0
    for item in list_keys:
        i += 1
        if int(message.text) == i:
            userSumFile.set_user_sum(message.chat.id, int(item))
            questionNumFile.set_question_num(message.chat.id, q_num + 1)
            check_answer(message)
            return


def result_handler(message):
    db_worker = SQLighter(config.database_name)
    t_num = testNumFile.get_test_num(message.chat.id)
    user_sum = userSumFile.get_user_sum(message.chat.id)

    for row in (db_worker.select_all_keys(t_num)):
        if int(row[2]) >= user_sum >= int(row[1]):
            bot.send_message(message.chat.id, row[0])
            reset(message)
            return

    bot.send_message(message.chat.id, "странно, твоего ответа нет")
    db_worker.close()
    reset(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    if message.text is None:
        return

    print(message.chat.id)
    db_worker = SQLighter(config.database_name)
    t_num = testNumFile.get_test_num(message.chat.id)
    q_num = questionNumFile.get_question_num(message.chat.id)
    if message.text == '/reset' or message.text == '/start':
        keyboard_hider = types.ReplyKeyboardRemove()
        db_worker.close()
        reset(message)
    elif t_num is None:
        bot.send_message(message.chat.id, 'Чтобы пройти тест напишите /start')
        db_worker.close()
    elif int(t_num) == 0:
        keyboard_hider = types.ReplyKeyboardRemove()
        db_worker.close()
        test_selector(message)
    elif q_num <= db_worker.question_amount(t_num):
        db_worker = SQLighter(config.database_name)
        text = str(db_worker.select_question(t_num, q_num)[3]) + '\n'
        a = '{}'.format(db_worker.select_question(t_num, q_num)[4])
        i = 0
        for item in a.split(','):
            i += 1
            text += str(i) + ') ' + item + '\n'
        markup = utils.generate_markup(i)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, question_handler)
        db_worker.close()
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        db_worker.close()
        result_handler(message)


if __name__ == '__main__':
    while True:
        try:
            random.seed()
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)  # или просто print(e) если у вас логгера нет,
            # или import traceback; traceback.print_exc() для печати полной инфы
            time.sleep(15)
