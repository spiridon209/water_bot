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
try:
    cur.executescript(sql)
except sqlite3.DatabaseError as err:
    print("make_db error", err)
else:
    print("Success")

cur.close()
con.close()
'''

    user_id INTEGER PRIMARY KEY,    #0
    chat_id REAL,                   #1
    name TEXT,                      #2
    gender TEXT,                    #3
    weight INTEGER,                 #4
    hometown TEXT,                  #5
    wakeup REAL,                    #6
    sleep REAL,                     #7
    daily_value_of_water INTEGER,   #8
    current_value_of_water INTEGER, #9
    time_zone Text,                 #10
    water_value_per_hour INTEGER,   #11
    bot_status TEXT,                #12
    reminder_time REAL              #13

'''