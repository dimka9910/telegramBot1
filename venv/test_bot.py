from __future__ import absolute_import
import unittest
from unittest import mock

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import Mockbot
from ptbtest import UserGenerator

from parser import parse_text


class TestBot2(unittest.TestCase):
    def setUp(self):
        self.bot = Mockbot()
        self.ug = UserGenerator()
        self.cg = ChatGenerator()
        self.mg = MessageGenerator(self.bot)
        self.updater = Updater(bot=self.bot)

    def test_start(self):
        def start(bot, update):
            text = 'Привет! Введи номер теста который хочешь пройти:\n'
            update.message.reply_text(text)

        self.updater.dispatcher.add_handler(CommandHandler("start", start))
        self.updater.start_polling()
        update = self.mg.get_message(text="/start")
        self.bot.insertUpdate(update)
        self.assertEqual(len(self.bot.sent_messages), 1)
        sent = self.bot.sent_messages[0]
        self.assertEqual(sent['method'], "sendMessage")
        self.assertEqual(sent['text'], "Привет! Введи номер теста который хочешь пройти:\n")
        self.updater.stop()

    def test_create(self):
        def create(bot, update):
            text = 'Чтобы добавить свой текст введите его в соответствуюшем формате:\n' \
               'Тест про кошек\n' \
               '1)Какая ты кошка?;глотка шорсный,пушистый,лысый;3,2,1\n' \
               '2)Где ты живешь?;спб,мск;1,0\n' \
               '3)Любишь бегать?;да,нет;1,0\n' \
               '4)Что любишь Кушать?;сосиски,молоко;2,1\n' \
               'Хороший кот;5;7\n' \
               'Нормальный кот;2;4\n' \
               'Не кот;0;1'
            update.message.reply_text(text)

        self.updater.dispatcher.add_handler(CommandHandler("create", create))
        self.updater.start_polling()
        update = self.mg.get_message(text="/create")
        self.bot.insertUpdate(update)
        self.assertEqual(len(self.bot.sent_messages), 1)
        sent = self.bot.sent_messages[0]
        self.assertEqual(sent['method'], "sendMessage")
        text = 'Чтобы добавить свой текст введите его в соответствуюшем формате:\n' \
               'Тест про кошек\n' \
               '1)Какая ты кошка?;глотка шорсный,пушистый,лысый;3,2,1\n' \
               '2)Где ты живешь?;спб,мск;1,0\n' \
               '3)Любишь бегать?;да,нет;1,0\n' \
               '4)Что любишь Кушать?;сосиски,молоко;2,1\n' \
               'Хороший кот;5;7\n' \
               'Нормальный кот;2;4\n' \
               'Не кот;0;1'
        self.assertEqual(sent['text'], text)
        self.updater.stop()

    def test_parser(self):
        @mock.patch('test_bot.parse_text', return_value="Вы что то не так ввели")
        def parser(bot, update, mock_parse_text):
            if update.message.text == '/reset' or update.message.text == '/start':
                return
            update.message.reply_text(parse_text(update.message.text))

        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, parser))
        self.updater.start_polling()
        update = self.mg.get_message(text="/reset")
        self.bot.insertUpdate(update)
        sent = self.bot.sent_messages
        self.assertEqual(sent.__len__(), 0)
        self.updater.stop()

        self.updater.start_polling()
        update = self.mg.get_message(text="NAME\n1)Question1;a,b;1,2")
        self.bot.insertUpdate(update)
        sent = self.bot.sent_messages
        self.assertEqual(sent[0]['method'], "sendMessage")
        self.assertEqual(sent[0]['text'], "Вы что то не так ввели")
        self.updater.stop()

if __name__ == '__main__':
    unittest.main()
