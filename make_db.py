# -*- coding: utf-8 -*-
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv('DB')
USER = os.getenv('USER')
PASS = os.getenv('PASS')
HOST = os.getenv('HOST')


def make_table(db=DB, user=USER, password=PASS, host=HOST):
    con = psycopg2.connect(dbname=db, user=user, password=password, host=host)
    cur = con.cursor()

    sql = "CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY, chat_id double precision, name text, gender text, weight integer," \
          "hometown text, wakeup real, sleep real, daily_value_of_water integer, current_value_of_water integer," \
          "time_zone text, water_value_per_hour integer, bot_status text, reminder_time real, user_state);"

    try:
        cur.execute(sql)
        con.commit()
    except Exception as err:
        print("make_db error", err)
    else:
        print("Success")

    cur.close()
    con.close()

if __name__ == '__main__':
    make_table()