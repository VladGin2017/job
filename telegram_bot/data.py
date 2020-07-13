import sqlite3

con = sqlite3.connect('data_base_of_tasks.db')
cor = con.cursor()

query = 'SELECT task_name FROM tasks'  # Задачи
cor.execute(query)
tasks = cor.fetchall()
list = []
for element in tasks:
    list.append(element[0])
tasks = list
del list

query_2 = 'SELECT id FROM tasks'  # id записи в БД
cor.execute(query_2)
id_ = cor.fetchall()
list = []
for element in id_:
    list.append(element[0])
id_ = list
del list

query_3 = 'SELECT duration FROM tasks'  # Срок задачи
cor.execute(query_3)
duration_ = cor.fetchall()
list = []
for element in duration_:
    list.append(element[0])
duration_ = list
del list

query_4 = 'SELECT finish FROM tasks'  # Дата окончания работы
cor.execute(query_4)
finish_ = cor.fetchall()
list = []
for element in finish_:
    list.append(element[0])
finish_ = list
del list

query_5 = 'SELECT start FROM tasks'  # Дата начала работы
cor.execute(query_5)
start_ = cor.fetchall()
list = []
for element in start_:
    list.append(element[0])
start_ = list
del list

query_6 = 'SELECT name FROM tasks'  # Имя пользователя
cor.execute(query_6)
name_ = cor.fetchall()
list = []
for element in name_:
    list.append(element[0])
name_ = list
del list

query_7 = 'SELECT id_user FROM tasks'  # id пользователя
cor.execute(query_7)
id_user = cor.fetchall()
list = []
for element in id_user:
    list.append(element[0])
id_user = list
del list

con.commit()
cor.close()