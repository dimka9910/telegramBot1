import sqlite3
from config import database_name

connection = sqlite3.connect(database_name)
cursor = connection.cursor()

cursor.execute('SELECT NameOfTest FROM test__name ORDER BY Id').fetchall()

text = "Привет"
num = 21
num2 = 12
sql = 'INSERT INTO tast__name (NameOfTest, TestCode, QuestionAmount) VALUES text, num, num2'
cursor.execute(sql)


connection.close()