#! /usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import patch
from parser import MyError
import re


def mock_parse_text(text):
    try:
        text = text.split('\n')
        line_number = 0
        line_number = line_number + 1

        regex = re.compile('^[0-9]{1,}\)')
        while regex.match(text[line_number]):
            array = text[line_number].split(')')
            question_number = int(array[0])
            question = array[1].split(';')

            answers = question[1].split(',')
            keys = question[2].split(',')
            i = 0
            j = 0
            for item in answers:
                i = i + 1
            for item in keys:
                j = j + 1
                if not item.isdecimal():
                    raise MyError('Ключи должны быть целыми числами!')
            if i != j:
                raise MyError('Количество ответов не соответствует количеству ключей!')

            line_number = line_number + 1

        while line_number < len(text):
            bracket = text[line_number].split(';')
            line_number = line_number + 1

    except IndexError:
        return "Выход за границы массива. Проверьте расстановку разделителей!"
    except Exception:
        return "Вы что то не так ввели"
    else:
        return "Парсинг успешен. База данных пополнена!"

@patch('parser.parse_text', side_effect=mock_parse_text)
class TestParser(TestCase):
    def test_parsed_successfully(self, parse_text):
      inputStr = 'Тест про кошек\n' \
               '1)Какая ты кошка?;глотка шорсный,пушистый,лысый;3,2,1\n' \
               '2)Где ты живешь?;спб,мск;1,0\n' \
               '3)Любишь бегать?;да,нет;1,0\n' \
               '4)Что любишь Кушать?;сосиски,молоко;2,1\n' \
               'Хороший кот;5;7\n' \
               'Нормальный кот;2;4\n' \
               'Не кот;0;1'
      expected = "Парсинг успешен. База данных пополнена!"
      self.assertEqual(parse_text(inputStr), expected)

    def test_parsing_failed(self, parse_text):
        inputStr = "NAME\n1)Question1;a,b;1,2"
        expected = "Выход за границы массива. Проверьте расстановку разделителей!"
        notExpected = "Парсинг успешен. База данных пополнена!"
        self.assertNotEqual(parse_text(inputStr), notExpected)
        self.assertEqual(parse_text(inputStr), expected)

    def test_parsing_something_is_wrong(self, parse_text):
        inputStr = "NAME\n1)Question1;a,b;a,b\n"
        expected = "Вы что то не так ввели"
        self.assertEqual(parse_text(inputStr), expected)
