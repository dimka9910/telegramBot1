# -*- coding: utf-8 -*-
import sqlite3
# файл отправляющий запросы к БД с тестами

class SQLighter:

    # инициализация
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # возвращает названия всех тестов
    def select_all_tests(self):
        with self.connection:
            return self.cursor.execute('SELECT NameOfTest FROM test__name ORDER BY Id').fetchall()

    # возвращает все ключи к заданному тесту
    def select_all_keys(self, test_code):
        with self.connection:
            return self.cursor.execute('SELECT Result, Low, High FROM test_keys WHERE TestCode = ?'
                                       , (test_code,)).fetchall()

    # возвращает общее количество тестов
    def test_len(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM test__name').fetchall()
            return len(result)

    # получает id всех тестов
    def select_test_code(self):
        with self.connection:
            return self.cursor.execute('SELECT Id FROM test__name ORDER BY Id').fetchall()

    # получает конкретный вопрос из теста по коду теста (id) и номеру вопроса
    def select_question(self, test_code, test_num):
        with self.connection:
            return self.cursor.execute('SELECT * FROM test_questions WHERE TestCode = ? AND QuestionNumber = ?'
                                       , (test_code, test_num,)).fetchall()[0]

    # получает общее количество вопросов по заданному тесту
    def question_amount(self, test_code):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM test_questions WHERE TestCode = ?', (test_code, )).fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()