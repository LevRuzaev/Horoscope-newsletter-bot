import telebot
import time
import csv
import os
from telebot import types
from threading import Thread
from stolen import horoscope
from datetime import datetime


def get_key(val):
    for key, value in marks.items():
        if val == value:
            return key

    return "key doesn't exist"


Users = {}
bot = telebot.TeleBot('6046688414:AAHX6u1hYY_OxzyOrXF8p4XloP_-zkxmvSE')


class User:
    def __init__(self, chat_id, first_name, message, admin):
        self.chat_id = chat_id
        self.first_name = first_name
        self.message = message
        self.admin = admin


marks = {
    'Овен♈': 'aries', 'Телец♉': 'taurus', 'Близнецы♊': 'gemini',
    'Рак♋': 'cancer', 'Лев♌': 'leo', 'Дева♍': 'virgo',
    'Весы♎': 'libra', 'Скорпион♏': 'scorpio', 'Стрелец♐': 'sagittarius',
    'Козерог♑': 'capricorn', 'Водолей♒': 'aquarius', 'Рыбы♓': 'pisces'}


# Приветственное сообщение, забирает id, с помощью кнопок перебрасывает дальше
@bot.message_handler(commands=['start', 'hi'])
def say_hi(message):
    Users[int(message.chat.id)] = User(int(message.chat.id), message.from_user.first_name, message, admin='No')
    person = False
    with open('data.csv', 'r', encoding='utf-8') as data:
        lines = data.readlines()
        for line in lines:
            if str(message.from_user.id) in line:
                global person_mark
                ID, username_, Name, person_mark, Admin = line.split(';')
                if Admin.strip() == 'Yes':
                    Users[message.chat.id].admin = 'Yes'
                if person_mark == 'None':
                    main_choose(message)
                    break
                else:
                    person = True
        if person:
            bot.send_message(Users[message.chat.id].chat_id,
                             f'Привет, {Users[message.chat.id].first_name}! Я тебя помню!')
            horo(Users[message.chat.id].message)
        else:
            append_user(Users[message.chat.id].message)


def append_user(message):
    with open('data.csv', 'a', encoding='utf-8', newline='') as data:
        writer = csv.writer(data, delimiter=';')
        if message.from_user.username == '':
            username = '_'
        else:
            username = message.from_user.username
        writer.writerow(
            [str(message.from_user.id), username, message.from_user.first_name, 'None', 'No'])
    new_player(Users[message.chat.id].message)


def new_player(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Хочу гороскоп!"))
    bot.send_message(Users[message.chat.id].chat_id,
                     f"Привет, {Users[message.chat.id].first_name}!", reply_markup=markup)

    bot.register_next_step_handler(message, main_choose)


# Выбор ЗЗ, перебрасывает в первый вывод гороскопа
def main_choose(message):
    markup = types.ReplyKeyboardMarkup()
    for key_ in marks:
        markup.add(types.KeyboardButton(key_))
    bot.send_message(message.chat.id, f"Пожалуйста, укажи знак зодиака:", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


# Первый вывод гороскопа, забираем ЗЗ в глобальный person_mark, далее гороскоп должен приходить автоматически каждый день
def on_click(message):
    if message.text not in marks.keys():
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton("Выбрать знак Зодиака"))
        bot.send_message(Users[message.chat.id], "Просто нажмите на кнопочку...", reply_markup=markup)
        bot.register_next_step_handler(message, main_choose)
    else:
        delete_buttons = types.ReplyKeyboardRemove()
        global person_mark
        person_mark = marks[message.text]
        with open('data.csv', 'r', encoding='utf-8') as data:
            DATA = data.readlines()

        for index_line in range(len(DATA)):
            if str(message.chat.id) in DATA[index_line]:
                line = DATA.pop(index_line)
                break

        content = line.split(';')
        content[3] = person_mark
        line = ';'.join(content)
        DATA.append(line)

        new_DATA = [row for row in DATA if row.count(';') == 4]
        with open('data.csv', 'w', encoding='utf-8') as data:
            data.writelines(new_DATA)

        with open('settings.txt', 'r', encoding='utf-8') as timing:
            sending_time = timing.read().strip()

        bot.send_message(Users[message.chat.id].chat_id,
                         f"{get_key(person_mark)[0:-1]}!\nТеперь каждый день в {sending_time} тебе будет приходить гороскоп",
                         reply_markup=delete_buttons)
        horo(Users[message.chat.id].message)


def horo(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Поменять Знак Зодиака"))
    if Users[message.chat.id].admin == 'Yes':
        markup.add(types.KeyboardButton("Админ-меню"))
    bot.send_message(Users[message.chat.id].chat_id,
                     f"Вот твой гороскоп на сегодня:\n\n{horoscope(person_mark)}", reply_markup=markup)
    bot.register_next_step_handler(Users[message.chat.id].message, boss_level)


def boss_level(message):
    if message.text in ["Админ-меню", "Назад"]:
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton("Все пользователи бота"))
        markup.add(types.KeyboardButton("Поменять время рассылки"))
        markup.add(types.KeyboardButton("Добавить пост к рассылке"))
        markup.add(types.KeyboardButton("Выйти"))
        bot.send_message(Users[message.chat.id].chat_id, f"Вы в меню", reply_markup=markup)
        bot.register_next_step_handler(message, menu)
    elif message.text == "Поменять Знак Зодиака":
        main_choose(Users[message.chat.id].message)
    else:
        horo(Users[message.chat.id].message)


def menu(message):
    if message.text == "Все пользователи бота":
        users(message)
    elif message.text == "Поменять время рассылки":
        change_sending_time_part_1(message)
    elif message.text == "Добавить пост к рассылке":
        post(message)
    else:
        horo(Users[message.chat.id].message)


def post(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Без фото"))
    bot.send_message(Users[message.chat.id].chat_id,
                     f"Пришлите сообщение, которое будет прикреплено к рассылке, сначала фото", reply_markup=markup)
    bot.register_next_step_handler(message, inter_photo)


def inter_photo(message):
    if message.text == "Без фото":
        if os.path.isfile('post.png'):
            os.remove('post.png')
        post_text(Users[message.chat.id].message)
    else:
        delete_buttons = types.ReplyKeyboardRemove()
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("post.png", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(Users[message.chat.id].chat_id,
                         f"Фото принято", reply_markup=delete_buttons)
        post_text(Users[message.chat.id].message)


def post_text(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Оставить текущий"))
    markup.add(types.KeyboardButton("Без текста"))
    bot.send_message(Users[message.chat.id].chat_id, f"Введите текст для рассылки", reply_markup=markup)
    bot.register_next_step_handler(message, get_text)


def get_text(message):
    if message.text == "Оставить текущий":
        end_post(Users[message.chat.id].message)
    elif message.text == "Без текста":
        open('post.txt', 'w').close()
        end_post(Users[message.chat.id].message)
    else:
        with open('post.txt', 'w', encoding='utf-8') as text:
            text.write(message.text)
        end_post(Users[message.chat.id].message)


def end_post(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Назад"))
    bot.send_message(Users[message.chat.id].chat_id, f"Сообщение добавленно в рассылку",
                     reply_markup=markup)
    bot.register_next_step_handler(Users[message.chat.id].message, boss_level)


def users(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Назад"))
    with open('data.csv', 'r', encoding='utf-8') as data:
        rows = csv.DictReader(data, delimiter=';')
        for row in rows:
            bot.send_message(Users[message.chat.id].chat_id, f"@{row['USERNAME']} - {row['NAME']}")
    bot.send_message(Users[message.chat.id].chat_id, f"На данный момент это все пользователи",
                     reply_markup=markup)
    bot.register_next_step_handler(Users[message.chat.id].message, boss_level)


def change_sending_time_part_1(message):
    delete_buttons = types.ReplyKeyboardRemove()
    bot.send_message(Users[message.chat.id].chat_id, f"Введите новое время рассылки в 24-часовом формате ЧЧ:ММ",
                     reply_markup=delete_buttons)
    bot.register_next_step_handler(Users[message.chat.id].message, change_sending_time_part_2)


def change_sending_time_part_2(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Назад"))
    with open('settings.txt', 'w', encoding='utf-8') as timing:
        timing.write(message.text)
    sending_time = message.text
    with open('data.csv', 'r', encoding='utf-8') as data:
        rows = csv.DictReader(data, delimiter=';')
        for row in rows:
            bot.send_message(int(row['ID']), f"Привет, {row['NAME']}! Время рассылки гороскопа было изменено")
            bot.send_message(int(row['ID']), f"Теперь гороскоп будет приходить в {sending_time}")
    bot.send_message(Users[message.chat.id].chat_id, f"Время рассылки изменено", reply_markup=markup)
    bot.register_next_step_handler(Users[message.chat.id].message, boss_level)


### Пассивная часть
# Ежедневная отправка гороскопа

def do_horo_every_day():
    with open('data.csv', 'r', encoding='utf-8') as data:
        rows = csv.DictReader(data, delimiter=';')
        for row in rows:
            if row['ID'].isdigit():
                bot.send_message(int(row['ID']), f"Привет, {row['NAME']}!")
                with open('post.txt', 'r', encoding='utf-8') as file:
                    text = file.read()
                try:
                    photo = open('post.png', 'rb')
                    bot.send_photo(int(row['ID']), photo,
                                   caption=f"{get_key(row['PERSON_MARK'])[-1]}Вот твой гороскоп на сегодня:\n\n{horoscope(row['PERSON_MARK'])}\n\n{text}")
                except IOError as e:
                    bot.send_message(int(row['ID']),
                                     f"{get_key(row['PERSON_MARK'])[-1]}Вот твой гороскоп на сегодня:\n\n{horoscope(row['PERSON_MARK'])}\n\n{text}")


def do_schedule():
    while True:
        with open('settings.txt', 'r', encoding='utf-8') as timing:
            sending_time = timing.read().strip()
        if datetime.strftime(datetime.now(), "%H:%M:%S") == sending_time + ':00':
            do_horo_every_day()
        time.sleep(1)


def main_loop():
    thread = Thread(target=do_schedule)
    thread.start()

    bot.polling(True)


if __name__ == '__main__':
    main_loop()
