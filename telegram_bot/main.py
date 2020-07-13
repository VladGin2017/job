import config
import telebot
import sqlite3
import datetime
from telebot import types
from datetime import datetime
import data

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])  # обработчик команды /start
def start(message):
    bot.send_message(message.chat.id, text="Привет" + '\n' + "Взять задачу /task" + '\n' + "Проверить статус задач \n"
                                                                                           "/status")


@bot.message_handler(commands=['task'])  # обработчик команды /task выдает пользвателю задачу
def task(message):
    global status
    for i in range(len(data.tasks)):
        bot.send_message(chat_id=data.id_user[i], text="Вам выдано задание: \n" +
                                              str(data.tasks[i]) + "\n" + "На выполнение этого задания есть "
                                              + str(data.duration_[i]) + " дня(дней)!")
        print(data.tasks[i])
        status = 'started'
        deadline = data.finish_[i]
        time_ = datetime.now().strftime("%Y-%m-%d")
        con = sqlite3.connect('data_base_of_tasks.db')
        cor = con.cursor()
        query = 'UPDATE tasks SET status = "В работе" WHERE id' + " = '" + str(data.id_[i]) + "'"
        cor.execute(query)
        con.commit()
        cor.close()

        if str(time_) < str(deadline):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            button_1 = types.InlineKeyboardButton(text="Завершить", callback_data="finish")
            keyboard.add(button_1)
            bot.send_message(chat_id=data.id_user[i], text="После выполнения задания нажмите кнопку 'Завершить'.",
                             reply_markup=keyboard)
        # print(time_)
        # print(deadline)
        while status == 'started' and str(time_) < str(deadline):
            time_ = datetime.now().strftime("%Y-%m-%d")
            status = status
            if status == 'finish':
                con = sqlite3.connect('data_base_of_tasks.db')
                cor = con.cursor()
                query = 'UPDATE tasks SET status = "Завершено" WHERE id' + " = '" + str(data.id_[i]) + "'"
                cor.execute(query)
                con.commit()
                cor.close()
        else:
            print("Task was updated!")
            if str(time_) > str(deadline):
                status = 'expired'
                con = sqlite3.connect('data_base_of_tasks.db')
                cor = con.cursor()
                query = 'UPDATE tasks SET status = "Просрочено" WHERE id' + " = '" + str(data.id_[i]) + "'"
                cor.execute(query)
                con.commit()
                cor.close()
                bot.send_message(chat_id=data.id_user[i], text="Задание было просрочено!")


@bot.callback_query_handler(func=lambda call: True)  # обработчик вызовов
def finish(call):
    global status
    if call.data == "finish":
        status = 'finish'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Задание завершено!')
        bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(commands='status')  # обработчик команды /status
def stat(message):
    con = sqlite3.connect('data_base_of_tasks.db')
    cor = con.cursor()
    query = 'SELECT status FROM tasks'
    cor.execute(query)
    statistic = cor.fetchall()
    list = []
    for element in statistic:
        list.append(element[0])
    statistic = list
    del list
    con.commit()
    cor.close()

    bot.send_message(message.chat.id, '\n'.join(['Пользователь: ' + data.name_[i] + '\n' + 'Статус задачи: ' + statistic[i]
                                                 + '\n' for i in range(len(statistic))]))
    del statistic


if __name__ == '__main__':
    bot.polling(none_stop=True)