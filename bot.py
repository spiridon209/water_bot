from collections import defaultdict
import time
from datetime import datetime, timezone, timedelta
import os

import config
from calculations import get_female_amount, get_male_amount, get_water_volume_per_hour
from model import check_user, create_data, bot_on, bot_off, check_bot_status, remove, add_reminder_time
import my_parser
from timezones import get_user_utc_0, get_current_utc_time
from model import get_message_text, get_info_about_active_users
from timeloop import Timeloop
from make_db import make_table

from dotenv import load_dotenv
import telebot
from telebot import types

load_dotenv()
DEBUG = os.getenv('DEBUG') == 'TRUE'
BOT_TOKEN = os.getenv('BOT_TOKEN')

#telebot.apihelper.proxy = config.proxy
bot = telebot.TeleBot(BOT_TOKEN)
make_table()
gender = ['Мужчина', 'Женщина']
control = ['1) Запустить бота', '2) Изменить данные о себе', '3) Остановить бота']
START, NAME, GENDER, WEIGHT, HOMETOWN, WAKEUP, SLEEP, DONE, FINISH = range(9)  # memory of bot

user_state = defaultdict(lambda: START)
info_about_user = {}  # data of user


def get_state(message):
    return user_state[message.chat.id]


def update_state(message, state):
    user_state[message.chat.id] = state


def create_gender_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=g, callback_data=g) for g in gender]
    keyboard.add(*buttons)
    return keyboard


def create_control_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=button, callback_data=button) for button in control]
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    id, name, value = check_user(message)

    if id == message.chat.id:
        update_state(message, DONE)
        bot.send_message(chat_id=message.chat.id,
                         text=f'Привет {name} ваша суточная норма потребления воды составляет {value}мл.')
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Привет, пожалуйста, скажите ваше имя, чтобы я знал как к вам обращаться.")
        update_state(message, NAME)

        info_about_user['id'] = message.chat.id


@bot.message_handler(func=lambda message: get_state(message) == NAME)
def get_user_name(message):
    keyboard = create_gender_keyboard()
    bot.send_message(chat_id=message.chat.id,
                     text=f"Рад познакомиться {message.text}!")
    name = message.text
    info_about_user['name'] = name
    update_state(message, GENDER)
    bot.send_message(chat_id=message.chat.id,
                     text=f"Пожалуйста укажите свой пол.", reply_markup=keyboard)


@bot.message_handler(func=lambda message: get_state(message) == WEIGHT)
def get_user_weight(message):
    try:
        weight = int(message.text)
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Упс, кажется данные введены не правильно, попробуйте еще раз. Пример ответа: 70")
    else:
        info_about_user['weight'] = weight
        bot.send_message(chat_id=message.chat.id,
                         text=f"В каком городе вы живете ?")
        update_state(message, HOMETOWN)


@bot.message_handler(func=lambda message: get_state(message) == HOMETOWN)
def get_user_hometown(message):
    hometown = message.text
    info_about_user['hometown'] = hometown
    user_time_zone = my_parser.get_utc(hometown)
    if user_time_zone == None:
        bot.send_message(chat_id=message.chat.id, text=f"Не могу найти город, возможно вы допустили ошибку в названии ?")
    else:
        info_about_user['time_zone'] = user_time_zone
        bot.send_message(chat_id=message.chat.id, text=f"Во сколько вы обычно просыпаетесь ?")
        update_state(message, WAKEUP)


@bot.message_handler(func=lambda message: get_state(message) == WAKEUP)
def get_user_wakeup_time(message):
    try:
        wakeup = float(message.text)
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Упс, кажется данные введены не правильно, попробуйте еще раз. Пример ответа: 8.30")
    else:
        info_about_user['wakeup'] = wakeup
        bot.send_message(chat_id=message.chat.id, text=f"Во сколько вы ложитесь спать ?")
        update_state(message, SLEEP)


@bot.message_handler(func=lambda message: get_state(message) == SLEEP)  # последний шаг, дальше расчет
def get_user_sleep_time(message):
    try:
        sleep = float(message.text)
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Упс кажется данные введены не правильно, попробуйте еще раз. Пример ответа: 22.30")
    else:
        info_about_user['sleep'] = sleep
        if info_about_user['gender'] == 'Мужчина':
            ans = get_male_amount(info_about_user['weight'])
        if info_about_user['gender'] == 'Женщина':
            ans = get_female_amount(info_about_user['weight'])
        bot.send_message(chat_id=message.chat.id, text=f"Готово! ваша суточная норма потребления воды составляет {ans}мл.")

        info_about_user['daily_value_of_water'] = ans
        info_about_user['current_value_of_water'] = ans
        info_about_user['water_value_per_hour'] = get_water_volume_per_hour(info_about_user['wakeup'],
                                                                             info_about_user['sleep'],
                                                                             info_about_user['daily_value_of_water'])

        wake_up_utc0, sleep_ust0 = get_user_utc_0(info_about_user['time_zone'], info_about_user['wakeup'],
                                                  info_about_user['sleep'])
        info_about_user['wakeup'] = wake_up_utc0
        info_about_user['sleep'] = sleep_ust0

        create_data(info_about_user)
        control_the_bot(message)


def control_the_bot(message):
    keyboard = create_control_keyboard()
    update_state(message, DONE)
    bot.send_message(chat_id=message.chat.id, text='Выберите нужную опцию.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda x: True)
def callback_gender_handler(callback_query):
    message = callback_query.message
    status = get_state(message)
    text = callback_query.data  # gender
    if status == GENDER:
        info_about_user['gender'] = text
        bot.answer_callback_query(callback_query_id=callback_query.id)
        bot.send_message(chat_id=message.chat.id, text="Отлично! Теперь введите свой вес в киллограммах(округлите до целых).")
        update_state(message, WEIGHT)

    if status == DONE:
        if text == '1) Запустить бота':
            bot_on(message)

            current_time = datetime.now(timezone.utc)
            time = str(current_time).split()[-1].split(':')
            reminder_time = round(float(f'{time[0]}.{time[1]}') + 0.1, 2)
            add_reminder_time(message, reminder_time)
            bot.send_message(chat_id=message.chat.id,
                             text="Бот запущен, теперь он будет напоминать пить воду каждый час!")

        if text == '2) Изменить данные о себе':
            status = check_bot_status(message)
            if status == 'on':
                bot.send_message(chat_id=message.chat.id, text='Сначала необходимо остановить бота!')
                control_the_bot(message)
            else:
                remove(message)
                update_state(message, START)
                bot.send_message(chat_id=message.chat.id, text='Кликнете на ---> /start в данном сообщении.')

        if text == '3) Остановить бота':
            bot_off(message)
            bot.send_message(chat_id=message.chat.id, text='Бот остановлен!')
            control_the_bot(message)


if __name__ == '__main__':

    tl = Timeloop()

    @tl.job(interval=timedelta(seconds=15))
    def send_message():
        current_time = get_current_utc_time()
        time = str(current_time).split()[-1].split(':')
        current_utc_time = float(f'{time[0]}.{time[1]}')
        list_of_users = get_info_about_active_users()

        for i in list_of_users:
            if i[-1] == current_utc_time:
                text = get_message_text(user_bio=i)
                try:
                    bot.send_message(chat_id=i[1], text=text)
                except Exception as ex:
                    print(f"Can't send message to user {i} ---> {ex}")

    tl.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            tl.stop()
            break
        break

    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=0)
        except KeyboardInterrupt:
            time.sleep(10)
