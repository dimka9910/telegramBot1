# -*- coding: utf-8 -*-
import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all_tests(self):
        with self.connection:
            return self.cursor.execute('SELECT NameOfTest FROM test__name ORDER BY Id').fetchall()

    def select_all_keys(self, test_code):
        with self.connection:
            return self.cursor.execute('SELECT Result, Low, High FROM test_keys WHERE TestCode = ?'
                                       , (test_code,)).fetchall()

    def test_len(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM test__name').fetchall()
            return len(result)

    def select_test_code(self):
        with self.connection:
            return self.cursor.execute('SELECT TestCode FROM test__name ORDER BY Id').fetchall()

    def select_question(self, test_code, test_num):
        with self.connection:
            return self.cursor.execute('SELECT * FROM test_questions WHERE TestCode = ? AND QuestionNumber = ?'
                                       , (test_code, test_num,)).fetchall()[0]

    def question_amount(self, test_code):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM test_questions WHERE TestCode = ?', (test_code, )).fetchall()
            return len(result)

    # def select_question_answers(self, test_code, test_num):
    #     with self.connection:
    #         return self.cursor.execute('SELECT Answers FROM test_questions WHERE TestCode = ? AND QuestionNumber = ?'
    #                                    , (test_code, test_num,)).fetchall()
    #
    # def select_question_keys(self, test_code, test_num):
    #     with self.connection:
    #         return self.cursor.execute('SELECT Keys FROM test_questions WHERE TestCode = ? AND QuestionNumber = ?'
    #                                    , (test_code, test_num,)).fetchall()


    def test_exist(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM test__name').fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
