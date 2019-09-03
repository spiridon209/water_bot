import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv('DB')
USER = os.getenv('USER')
PASS = os.getenv('PASS')
HOST = os.getenv('HOST')


def check_user(message, db=DB, user=USER, password=PASS, host=HOST):
    """The function checks the presence of the user in the database."""

    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"SELECT chat_id from users WHERE chat_id={message.chat.id}")
        id = cur.fetchone()[0]
        cur.execute(f"SELECT name from users WHERE chat_id={id}")
        name = cur.fetchone()[0]
        cur.execute(f"SELECT daily_value_of_water from users WHERE chat_id={id}")
        value = cur.fetchone()[0]
        cur.close()
        con.close()

    except Exception:
        id = 0
        name = ''
        value = 0
        cur.close()
        con.close()

    return id, name, value


def create_data(data, db=DB, user=USER, password=PASS, host=HOST):
    id = data['id']
    name = data['name']
    gender = data['gender']
    weight = data['weight']
    hometown = data['hometown']
    wakeup = data['wakeup']
    sleep = data['sleep']
    daily_value_of_water = data['daily_value_of_water']
    current_value_of_water = data['current_value_of_water']
    time_zone = data['time_zone']
    water_value_per_hour = data['water_value_per_hour']
    bot_status = 'off'
    user_state = 'wake'
    reminder_time = 0

    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"INSERT INTO users (chat_id, name, gender, weight, hometown, wakeup, sleep, daily_value_of_water, "
                    f"current_value_of_water, time_zone, water_value_per_hour, bot_status, reminder_time, user_state) "
                    f"VALUES({id}, '{name}', '{gender}', {weight}, '{hometown}', {wakeup}, {sleep}, "
                    f"{daily_value_of_water}, {current_value_of_water}, '{time_zone}', "
                    f"{water_value_per_hour}, '{bot_status}', {reminder_time}, '{user_state}')")
        con.commit()
        print('Table is created!')

    except Exception as ex:
        print(f'Create error {ex}')

    finally:
        cur.close()
        con.close()



def remove(message, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"DELETE from users WHERE chat_id={message.chat.id}")
        con.commit()

    except Exception:
        cur.close()
        con.close()
        print('Remove error')


def check_bot_status(message, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"SELECT bot_status from users WHERE chat_id={message.chat.id}")
        bot_status = cur.fetchone()[0]
        return bot_status

    except Exception as ex:
        print(f"Can't check bot_status - {ex}")

    finally:
        cur.close()
        con.close()


def bot_off(message, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()
    status = 'off'
    try:
        cur.execute(f"UPDATE users SET bot_status='{status}' WHERE chat_id={message.chat.id}")
        con.commit()

    except Exception as ex:
        print(f"Can't stop the bot - {ex}")

    finally:
        cur.close()
        con.close()
        return


def bot_on(message, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()
    status = 'on'
    try:
        cur.execute(f"UPDATE users SET bot_status='{status}' WHERE chat_id={message.chat.id}")
        con.commit()

    except Exception as ex:
        print(f"Can't start the bot - {ex}")

    finally:
        cur.close()
        con.close()
        return


def update_values_of_water(user_id, daily_value, current_value, value_per_hour, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        current_value -= value_per_hour

        if current_value <= 0:
            cur.execute(f"UPDATE users SET current_value_of_water={0} WHERE user_id={user_id}")
            con.commit()
        else:
            cur.execute(f"UPDATE users SET current_value_of_water={current_value} WHERE user_id={user_id}")  # возможно сделать изменение тут чтобы не писать в базу когда не надо
            con.commit()

        cur.close()
        con.close()

    except Exception:
        print('Update error')
        cur.close()
        con.close()


def get_info_about_active_users(db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"SELECT * from users WHERE bot_status='on'")
        data_from_db = cur.fetchall()
        cur.close()
        con.close()
        return data_from_db

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't get chat_id and reminder_time from db ---> {ex}")


def add_reminder_time(message, reminder_time, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    if int(reminder_time) == 24:
        reminder_time = round(0 + (reminder_time % int(reminder_time)), 2)

    if reminder_time - int(reminder_time) == 0.6:
        reminder_time = int(reminder_time) + 1

    try:
        cur.execute(f"UPDATE users SET reminder_time={reminder_time} WHERE chat_id={message.chat.id}")
        con.commit()
        cur.close()
        con.close()

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't add reminder_time db ---> {ex}")


def update_reminder_time(new_time, user_id, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    if int(new_time) == 24:
        new_time = round(0 + (new_time % int(new_time)), 2)

    if new_time - int(new_time) == 0.6:
        new_time = int(new_time) + 1

    try:
        cur.execute(f"UPDATE users SET reminder_time={new_time} WHERE user_id={user_id}")
        con.commit()
        cur.close()
        con.close()

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't update reminder_time db ---> {ex}")


def reset_current_value(user_id, daily_value_of_water, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"UPDATE users SET current_value_of_water={daily_value_of_water} WHERE user_id={user_id}")
        con.commit()

    except Exception:
        print('Reset current value of water error')

    finally:
        cur.close()
        con.close()
        return


def update_user_state_to_sleep(user_id, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"UPDATE users SET user_state='sleep' WHERE user_id={user_id}")
        con.commit()
        cur.close()
        con.close()

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't update user_state to sleep db ---> {ex}")


def update_user_state_to_wake(user_id, db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    try:
        cur.execute(f"UPDATE users SET user_state='wake' WHERE user_id={user_id}")
        con.commit()
        cur.close()
        con.close()

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't update user_state to wake db ---> {ex}")


def get_message_text(user_bio, current_utc_time):

    '''
    :return: The message that will be sent to a user
    '''

    sleep = user_bio[7]
    wakeup = user_bio[6]
    user_time = user_bio[-2]
    daily_value_of_water = user_bio[8]
    current_value_of_water = user_bio[9]
    water_value_per_hour = user_bio[11]
    user_state = user_bio[-1]

    if current_utc_time == wakeup and user_state == 'sleep':
        current_value_of_water -= user_bio[-4]
        text = f'Доброе утро! Пора выпить {user_bio[-4]}мл воды, осталось {current_value_of_water}мл.'
        update_values_of_water(user_id=user_bio[0], daily_value=daily_value_of_water,
                               current_value=user_bio[9], value_per_hour=user_bio[11])
        update_reminder_time(new_time=round(user_bio[-2] + 1, 2), user_id=user_bio[0])
        update_user_state_to_wake(user_id=user_bio[0])
        return text

    elif current_value_of_water <= 0 and user_state == 'wake':
        text = 'Сегодня вы употребили свою суточную норму воды, хорошая работа!'
        update_reminder_time(new_time=wakeup, user_id=user_bio[0])
        reset_current_value(user_id=user_bio[0], daily_value_of_water=daily_value_of_water)
        update_user_state_to_sleep(user_id=user_bio[0])
        return text

    elif current_utc_time == sleep and current_value_of_water > 0 and user_state == 'wake':
        text = f'Сегодня вы употребили не достаточно воды. Ничего страшного! Завтра у вас всё получится!'
        reset_current_value(user_id=user_bio[0], daily_value_of_water=daily_value_of_water)
        update_reminder_time(new_time=wakeup, user_id=user_bio[0])
        update_user_state_to_sleep(user_id=user_bio[0])
        return text

    elif current_utc_time == user_time and user_state == 'wake':
        current_value_of_water -= water_value_per_hour

        if current_value_of_water - water_value_per_hour < 0:
            last_value_of_water = current_value_of_water + water_value_per_hour
            text = f'Пора выпить {last_value_of_water}мл воды, осталось 0мл.'
            update_values_of_water(user_id=user_bio[0], daily_value=daily_value_of_water,
                                   current_value=user_bio[9], value_per_hour=user_bio[11])
            update_reminder_time(new_time=sleep, user_id=user_bio[0])
        else:
            text = f'Пора выпить {user_bio[-4]}мл воды, осталось {current_value_of_water}мл.'
            update_values_of_water(user_id=user_bio[0], daily_value=daily_value_of_water,
                                   current_value=user_bio[9], value_per_hour=user_bio[11])
            update_reminder_time(new_time=round(user_time + 1, 2), user_id=user_bio[0])
        return text
