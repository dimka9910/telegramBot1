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
    reset(message)  # сбрасываем
    bot.send_message(message.chat.id, 'Привет! Введи номер теста который хочешь пройти')
    testNumFile.set_test_num(message.chat.id, 0)
    db_worker = SQLighter(config.database_name)
    text = ''
    i = 1
    # выводим список тестов
    for row in (db_worker.select_all_tests()):
        text += str(i) + ") " + str(row[0]) + '\n'
        i += 1
    bot.send_message(message.chat.id, text)
    db_worker.close()


@bot.message_handler(commands=['reset'])
def reset(message):
    # сбрасываем все данные пользователя в бд
    testNumFile.reset_test_num(message.chat.id)
    questionNumFile.reset_question_num(message.chat.id)
    userSumFile.reset_user_sum(message.chat.id)
    # check_answer(message)


def test_selector(message):
    db_worker = SQLighter(config.database_name)
    # так же банальные проверки
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Введи пожалуйста номер теста :)")
        db_worker.close()
        return
    if int(message.text) > db_worker.test_len():
        bot.send_message(message.chat.id, "Такого номера нет в списке :(")
        db_worker.close()
        return

    # тк айдишники не обязательно идут по порядку, и не обязательно с первого
    # ты мы пробегаемся по всем тестам увеличевая переменную i
    # и если номер теста по порядку совпал с чисом ведённым пользователем
    # присваиваем ему этот номер
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
    # так как этот метод принимает новое сообщение
    # тут нужны те же две проверки
    if message.text is None:
        return

    if message.text == '/reset' or message.text == '/start':
        types.ReplyKeyboardRemove()
        start(message)
        return

    # так же проверка что пользователь отправил именно число
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Введите число с клавиатуры")
        check_answer(message)
        return

    db_worker = SQLighter(config.database_name)
    t_num = testNumFile.get_test_num(message.chat.id)
    q_num = questionNumFile.get_question_num(message.chat.id)

    # похожим образом получаем данные теперь из 5й колонки, теперь это у нас числа с ключами
    # заодно считаем сколько у нас всего ключей (= сколько ответов)
    i = 0
    k = '{}'.format(db_worker.select_question(t_num, q_num)[5])
    list_keys = []
    for item in k.split(','):
        i += 1 # в эту переменную
        list_keys.append(item)

    db_worker.close()

    # и если пользователь ввёл число не из всплывающей клавиатуры а больше или меньше
    # снова ругаемся
    if int(message.text) < 1 or int(message.text) > i:
        bot.send_message(message.chat.id, "Такого варианта ответа нет")
        check_answer(message)
        return

    # если же всё окей, снова пробегаемся по всем ключам
    i = 0
    for item in list_keys:
        i += 1
        if int(message.text) == i:  # и если текст сообщения равен номеру ответа
            userSumFile.set_user_sum(message.chat.id, int(item))  # прибавляем к сумме значение соответствующего ключа
            questionNumFile.set_question_num(message.chat.id, q_num + 1)  # и увеличиваем номер вопроса пользователя
            check_answer(message)  # и отправляем текущее сообщение на чек ансвер
            # в этот раз не регистр некст стэп потому что нам нужен ответ сразу же, на текущее сообщение пользователя
            # метод check_answer видит номер следующего вопроса, и высылает сразу следующий вопрос с новыми
            # вариантами ответов, после чего метод question_handler снова ждёт новый ответ
            return


def result_handler(message):
    db_worker = SQLighter(config.database_name)
    t_num = testNumFile.get_test_num(message.chat.id)
    user_sum = userSumFile.get_user_sum(message.chat.id)

    for row in (db_worker.select_all_keys(t_num)):
        if int(row[2]) >= user_sum >= int(row[1]):
            bot.send_message(message.chat.id, "Ваш результат: \n\n" + row[0])
            reset(message)
            return

    bot.send_message(message.chat.id, "странно, твоего ответа нет")
    db_worker.close()
    reset(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # защита от нетекстовых сообщений (картинки и прочее)
    if message.text is None:
        return
    print(message.chat.id)
    # открываем соединение с бд
    db_worker = SQLighter(config.database_name)
    # получаем номер теста и номер вопроса пользователя
    t_num = testNumFile.get_test_num(message.chat.id)
    q_num = questionNumFile.get_question_num(message.chat.id)
    if message.text == '/reset' or message.text == '/start':  # на случай если пользователь решил прервать тест
        keyboard_hider = types.ReplyKeyboardRemove()
        db_worker.close()
        reset(message)  # сбрасываем данные пользователя
    elif t_num is None:  # если в ячейки ничего нет, то возвращается none, это означает что пользователь не выбрал тест
        bot.send_message(message.chat.id, 'Чтобы пройти тест напишите /start')
        db_worker.close()
    elif int(t_num) == 0:
        # нулевой тест появляется после команды старт, это означает что пользователь набрал номер
        # теста и это надо обработать методом тест селектор
        keyboard_hider = types.ReplyKeyboardRemove() # прячем клавиатуру
        db_worker.close()
        test_selector(message)
    elif q_num <= db_worker.question_amount(t_num):
        # пока номер вопроса меньше или равен количеству вопросов
        # пользователь получает новые вопросы
        db_worker = SQLighter(config.database_name)
        # из бд получаем строчку с заданным вопросом
        # как видно по схеме бд третья колонка это как раз таки сам вопрос, мы его и добавояем в переменную
        # text
        text = str(db_worker.select_question(t_num, q_num)[3]) + '\n'
        # а затем мы берем данные из 4й колонки, где сами варианты ответов
        a = '{}'.format(db_worker.select_question(t_num, q_num)[4])
        i = 0
        # и пробегая по этой строке указав что данные разделены через запятую
        # мы добавляем в переменную текст варианты ответов
        for item in a.split(','):
            i += 1
            text += str(i) + ') ' + item + '\n'
        # генерируем раскладку клавиатуры с таким количеством вариантов ответов
        markup = utils.generate_markup(i)
        # и отправляем сообщение где последний параметр это раскладка клавиатуры
        bot.send_message(message.chat.id, text, reply_markup=markup)
        # этот метод означает что на следующем шаге сообщение пойдёт в метод
        # question_handler минуя check_answer
        bot.register_next_step_handler(message, question_handler)
        db_worker.close()
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        db_worker.close()
        # в случае когда тест начат, вопросы закончились, идём на метод обработки результатов
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
