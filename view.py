import sqlite3
import time
from datetime import timedelta

from timezones import get_current_utc_time
from model import get_message_text, get_info_about_active_users

from timeloop import Timeloop


def send_message_per_hour(bot):
    tl = Timeloop()

    @tl.job(interval=timedelta(seconds=15))
    def send_message():
        current_time = get_current_utc_time()
        time = str(current_time).split()[-1].split(':')
        current_utc_time = float(f'{time[0]}.{time[1]}')
        list_of_users = get_info_about_active_users()

        for i in list_of_users:
            print('send_message')
            print(current_utc_time)
            print(i[13])
            if i[-1] == current_utc_time:
                text = get_message_text(user_bio=i)
                bot.send_message(chat_id=i[1], text=text)

    tl.start()

    while True:
        try:
            time.sleep(1)
        except Exception as ex:
            print(ex)
            tl.stop()
            break

"Сейчас(вроде) всё время хранится в ютс0 тут надо получать chat_id, reminder_time, всех юзеров у которых" \
"бот статус = ОН, далее сравниваем совпадает ли текущее время с reminder_time если да то шлем сообшение и увеличиваем время на 1." \
"как то надо учесть шоб время ставилось на wake_up если выпита норма или уже поздно"

