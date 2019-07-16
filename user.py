import sqlite3
# Work with database
class User:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.gender = data['gender']
        self.weight = data['weight']
        self.hometown = data['hometown']
        self.wakeup = data['wakeup']
        self.sleep = data['sleep']
        self.daily_value_of_water = data['daily_value_of_water']
        self.current_value_of_water = data['current_value_of_water']
        self.time_zone = data['time_zone']
        self.water_value_per_hour = data['water_value_per_hour']
        self.bot_status = data['bot_status']
        self.reminder_time = data['reminder_time']
        self.create()

    def create(self):
        con = sqlite3.connect("bot.db")
        cur = con.cursor()

        try:
            cur.execute(f'INSERT INTO user VALUES(NULL, {self.id}, "{self.name}", "{self.gender}", {self.weight}, '
                        f'"{self.hometown}", {self.wakeup}, {self.sleep}, {self.daily_value_of_water},'
                        f'{self.current_value_of_water}, "{self.time_zone}", {self.water_value_per_hour},'
                        f'"{self.bot_status}", {self.reminder_time})')
            con.commit()

        except Exception as ex:
            print(f'Create error {ex}')

        finally:
            cur.close()
            con.close()

    @staticmethod
    def update_reminder_time(message, reminder_time): # реализовать
        pass


    @staticmethod
    def update(message):
        con = sqlite3.connect("bot.db")
        cur = con.cursor()

        try:
            cur.execute(f'SELECT daily_value_of_water from user WHERE chat_id={message.chat.id}')
            daily = cur.fetchone()[0]

            cur.execute(f'SELECT current_value_of_water from user WHERE chat_id={message.chat.id}')
            current = cur.fetchone()[0]

            cur.execute(f'SELECT water_value_per_hour from user WHERE chat_id={message.chat.id}')
            value = cur.fetchone()[0]

            cur.execute(f'SELECT sleep from user WHERE chat_id={message.chat.id}')
            sleep = cur.fetchone()[0]

            cur.execute(f'SELECT wakeup from user WHERE chat_id={message.chat.id}')
            wakeup = cur.fetchone()[0]

            # cur.execute(f'SELECT reminder_time from user WHERE chat_id={message.chat.id}')
            # reminder_time = cur.fetchone()[0]

            current -= value

            if value > current:
                cur.execute(f'UPDATE user SET current_value_of_water={daily} WHERE chat_id={message.chat.id}')
                con.commit()
            else:
                cur.execute(f'UPDATE user SET current_value_of_water={current} WHERE chat_id=({message.chat.id})') # возможно сделать изменение тут чтобы не писать в базу когда не надо
                con.commit()

            cur.close()
            con.close()
            return value, current, sleep, wakeup #reminder_time

        except Exception:
            print('Update error')
            cur.close()
            con.close()

    @staticmethod
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

    @staticmethod
    def update_current_value(message):
        con = sqlite3.connect("bot.db")
        cur = con.cursor()

        try:
            cur.execute(f'SELECT daily_value_of_water from user WHERE chat_id={message.chat.id}')
            daily = cur.fetchone()[0]
            cur.execute(f'UPDATE user SET current_value_of_water={daily} WHERE chat_id={message.chat.id}')
            con.commit()

        except Exception:
            print('Update current value of water error')

        finally:
            cur.close()
            con.close()
            return

    @staticmethod
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

    @staticmethod
    def off_bot(message):
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

    @staticmethod
    def on_bot(message):
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
