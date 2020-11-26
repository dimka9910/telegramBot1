# -*- coding: utf-8 -*-
# Этот токен невалидный, можете даже не пробовать :)
from enum import Enum

token = '1412812430:AAFzm-JeVW6wVuusHA8F79OUJ9ICLmkj6cY'
shelve_name = 'shelve.db'  # Файл с хранилищем
questionNum = 'questionNum.db'  # Файл с хранилищем
testNum = 'testNum.db'  # Файл с хранилищем
userSum = 'userSum.db'  # Файл с хранилищем
database_name = 't.db'  # Файл с базой данных
db_file = "database.vdb"

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_SELECTING_TEST = "1"
    S_SOLVING_TEST = "2"
    S_SHOW_RESULT = "3"
