# -*- coding: utf-8 -*-
import sqlite3
# make database
con = sqlite3.connect("bot.db")
cur = con.cursor()

sql = '''
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,
    chat_id REAL,
    name TEXT,
    gender TEXT,
    weight INTEGER,
    hometown TEXT,
    wakeup REAL,
    sleep REAL,
    daily_value_of_water INTEGER,
    current_value_of_water INTEGER,
    time_zone Text,
    water_value_per_hour INTEGER,
    bot_status TEXT,
    reminder_time REAL
);
'''


if __name__ == '__main__':

    try:
        cur.executescript(sql)
    except sqlite3.DatabaseError as err:
        print("make_db error", err)
    else:
        print("Success")

    cur.close()
    con.close()
