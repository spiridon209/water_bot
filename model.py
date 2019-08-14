import sqlite3


def check_user(message):
    """The function checks the presence of the user in the database."""

    con = sqlite3.connect('bot.db')
    cur = con.cursor()

    try:
        cur.execute(f'SELECT chat_id from user WHERE chat_id={message.chat.id}')
        id = cur.fetchone()[0]
        cur.execute(f'SELECT name from user WHERE chat_id={id}')
        name = cur.fetchone()[0]
        cur.execute(f'SELECT daily_value_of_water from user WHERE chat_id={id}')
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


def create_data(data):
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
    reminder_time = 0

    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        cur.execute(f'INSERT INTO user VALUES(NULL, {id}, "{name}", "{gender}", {weight}, '
                    f'"{hometown}", {wakeup}, {sleep}, {daily_value_of_water},'
                    f'{current_value_of_water}, "{time_zone}", {water_value_per_hour},'
                    f'"{bot_status}", {reminder_time})')
        con.commit()

    except Exception as ex:
        print(f'Create error {ex}')

    finally:
        cur.close()
        con.close()



def remove(message):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        cur.execute(f'DELETE from user WHERE chat_id={message.chat.id}')
        con.commit()

    except Exception:
        cur.close()
        con.close()
        print('Remove error')


def check_bot_status(message):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        cur.execute(f'SELECT bot_status from user WHERE chat_id={message.chat.id}')
        bot_status = cur.fetchone()[0]
        return bot_status

    except Exception as ex:
        print(f"Can't check bot_status - {ex}")

    finally:
        cur.close()
        con.close()


def bot_off(message):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    status = "'off'"
    try:
        cur.execute(f'UPDATE user SET bot_status={status} WHERE chat_id={message.chat.id}')
        con.commit()

    except Exception as ex:
        print(f"Can't stop the bot - {ex}")

    finally:
        cur.close()
        con.close()
        return


def bot_on(message):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    status = "'on'"
    try:
        cur.execute(f'UPDATE user SET bot_status={status} WHERE chat_id={message.chat.id}')
        con.commit()

    except Exception as ex:
        print(f"Can't stop the bot - {ex}")

    finally:
        cur.close()
        con.close()
        return


def update_values_of_water(user_id, daily_value, current_value, value_per_hour):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        current_value -= value_per_hour

        if value_per_hour > current_value:
            cur.execute(f'UPDATE user SET current_value_of_water={daily_value} WHERE user_id={user_id}')
            con.commit()
        else:
            cur.execute(f'UPDATE user SET current_value_of_water={current_value} WHERE user_id={user_id}')  # возможно сделать изменение тут чтобы не писать в базу когда не надо
            con.commit()

        cur.close()
        con.close()

    except Exception:
        print('Update error')
        cur.close()
        con.close()


def get_info_about_active_users():
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        cur.execute(f'SELECT * from user WHERE bot_status="on"')
        data_from_db = cur.fetchall()
        cur.close()
        con.close()
        return data_from_db

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't get chat_id and reminder_time from db ---> {ex}")


def add_reminder_time(message, reminder_time):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    if reminder_time % int(reminder_time) == 0.6:
        reminder_time = int(reminder_time) + 1

    try:
        cur.execute(f'UPDATE user SET reminder_time={reminder_time} WHERE chat_id={message.chat.id}')
        con.commit()
        cur.close()
        con.close()

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't add reminder_time db ---> {ex}")


def update_reminder_time(new_time, user_id):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    if new_time % int(new_time) == 0.6:
        new_time = int(new_time) + 1

    try:
        cur.execute(f'UPDATE user SET reminder_time={new_time} WHERE user_id={user_id}')
        con.commit()
        cur.close()
        con.close()

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't update reminder_time db ---> {ex}")


def reset_current_value(user_id, daily_value_of_water):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        cur.execute(f'UPDATE user SET current_value_of_water={daily_value_of_water} WHERE user_id={user_id}')
        con.commit()

    except Exception:
        print('Reset current value of water error')

    finally:
        cur.close()
        con.close()
        return


def get_message_text(user_bio, current_utc_time):

    '''
    :return: The message that will be sent to a user
    '''

    sleep = user_bio[7]
    wakeup = user_bio[6]
    user_time = user_bio[-1]
    current_value_of_water = user_bio[9]

    if user_time == wakeup:
        current_value_of_water -= user_bio[-3]
        text = f'Доброе утро! Пора выпить {user_bio[-3]}мл воды, осталось {current_value_of_water}мл.'
        update_values_of_water(user_id=user_bio[0], daily_value=user_bio[8],
                               current_value=user_bio[9], value_per_hour=user_bio[11])
        update_reminder_time(new_time=round(user_bio[-1] + 1, 2), user_id=user_bio[0])
        return text

    elif current_value_of_water <= 0:
        text = 'Сегодня вы употребили свою суточную норму воды, хорошая работа!'
        update_reminder_time(new_time=user_bio[6], user_id=user_bio[0])
        reset_current_value(user_id=user_bio[0], daily_value_of_water=user_bio[8])
        return text

    elif current_utc_time == sleep and current_value_of_water > 0:
        text = f'Сегодня вы употребили не достаточно воды. Ничего страшного! Завтра у вас всё получится!'
        reset_current_value(user_id=user_bio[0], daily_value_of_water=user_bio[8])
        update_reminder_time(new_time=user_bio[6], user_id=user_bio[0])
        return text

    else:
        current_value_of_water -= user_bio[-3]
        text = f'Пора выпить {user_bio[-3]}мл воды, осталось {current_value_of_water}мл.'
        update_values_of_water(user_id=user_bio[0], daily_value=user_bio[8],
                               current_value=user_bio[9], value_per_hour=user_bio[11])
        update_reminder_time(new_time=round(user_bio[-1] + 1, 2), user_id=user_bio[0])
        return text
