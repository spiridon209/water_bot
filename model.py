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
    reminder_time = data['reminder_time']

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

    except Exception:
        print('Remove error')

    finally:
        con.commit()
        cur.close()
        con.close()
        return


# def update_current_value(message):
#     con = sqlite3.connect("bot.db")
#     cur = con.cursor()
#
#     try:
#         cur.execute(f'SELECT daily_value_of_water from user WHERE chat_id={message.chat.id}')
#         daily = cur.fetchone()[0]
#         cur.execute(f'UPDATE user SET current_value_of_water={daily} WHERE chat_id={message.chat.id}')
#         con.commit()
#
#     except Exception:
#         print('Update current value of water error')
#
#     finally:
#         cur.close()
#         con.close()
#         return


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


def update_values_of_water(chat_id, daily_value, current_value, value_per_hour):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        current_value -= value_per_hour

        if value_per_hour > current_value:
            cur.execute(f'UPDATE user SET current_value_of_water={daily_value} WHERE chat_id={chat_id}')
            con.commit()
        else:
            cur.execute(f'UPDATE user SET current_value_of_water={current_value} WHERE chat_id={chat_id}')  # возможно сделать изменение тут чтобы не писать в базу когда не надо
            con.commit()

        cur.close()
        con.close()

    except Exception:
        print('Update error')
        cur.close()
        con.close()


def get_reminder_time():
    con = sqlite3.connect("bot.db")
    cur = con.cursor()

    try:
        cur.execute(f'SELECT chat_id, reminder_time from user WHERE bot_status=on')
        data_from_db = cur.fetchall()
        cur.close()
        con.close()
        return data_from_db

    except Exception as ex:
        cur.close()
        con.close()
        print(f"Can't get chat_id and reminder_time from db ---> {ex}")



