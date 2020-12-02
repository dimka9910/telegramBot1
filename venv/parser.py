import sqlite3
import re
import config


def parse_text(text):
    try:
        conn = sqlite3.connect(config.database_name)
        cursor = conn.cursor()

        # filename = input("Введите название текстового файла: ")
        # file = open(filename, 'r', encoding='utf-8')
        # text = file.read()
        # file.close()
        text = text.split('\n')  # представили текст в виде кортежа: один элемент = одна строка текстового файла
        # нулевую строку сохраняем в БД как название теста
        line_number = 0
        test_name = text[line_number]
        test_name_query = "INSERT INTO test__name(NameOfTest) VALUES (?)"
        cursor.execute(test_name_query, [test_name])
        test_id_query = "SELECT Id FROM test__name WHERE NameOfTest = ?"
        test_id = cursor.execute(test_id_query, [test_name]).fetchall()[0][0]  # получаем айдишник текущего теста
        line_number = line_number + 1

        # начинаем сохранять вопросы в БД, если строка начинается с числа со скобкой
        question_query = "INSERT INTO test_questions(TestCode, QuestionNumber, Question, Answers, Keys) VALUES (?, ?, ?, ?, ?)"
        regex = re.compile('^[0-9]{1,}\)')  # регулярное выражение типа "строка начинается с числа и скобки"
        while regex.match(text[line_number]):  # цикл работает пока строка начинается с число)
            array = text[line_number].split(')')  # делим строку на часть до скобки и после
            question_number = int(array[0])  # то что до скобки - номер вопроса
            question = array[1].split(';')  # делим то что после скобки при помощи точки с запятой
            full_question = [test_id, question_number, question[0], question[1],
                             question[2]]  # кортеж со всеми полями в БД
            cursor.execute(question_query, full_question)  # сохранили в БД
            line_number = line_number + 1

        # когда закончились числа со скобкой, начинаем заполнять таблицу с ключами
        key_query = "INSERT INTO test_keys(TestCode, Result, Low, High) VALUES (?, ?, ?, ?)"
        while line_number < len(text):  # сохраняем, пока не закончится файл
            bracket = text[line_number].split(';')  # делим всю строку при помощи точки с запятой
            full_key = [test_id, bracket[0], int(bracket[1]), int(bracket[2])]  # кортеж со всеми полями в БД
            cursor.execute(key_query, full_key)  # сохранили в БД
            line_number = line_number + 1

        conn.commit()  # сохраняем все изменения в БД
        conn.close()

    except IndexError:
        return "Выход за границы массива. Проверьте расстановку разделителей!"
    except sqlite3.OperationalError:
        return "Неудачное сохранение в базу данных!"
    except sqlite3.IntegrityError:
        return "Тест с таким названием уже есть в БД!"
    except Exception:
        print(Exception.__traceback__)
    else:
        return "Парсинг успешен. База данных пополнена!"
