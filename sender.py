
import time
from timeloop import Timeloop
from datetime import timedelta, datetime

from user import User
from timezones import UserTimeZone, time_zones_russia


class Myloop(Timeloop):

    def clear_my_jobs(self):
        self.jobs = []

    def stop(self):
        self._stop_jobs()
        self.clear_my_jobs()
        self.logger.info("Timeloop exited.")


# попробовать другие модули
def send_message_per_hour(bot, message, status):

    def start():
        tl = Myloop()

        @tl.job(interval=timedelta(seconds=15))
        def sample_job_every_1h():

            value, current, sleep, wakeup, time_zone = User.update(message)
            # print(value,sleep,wakeup)
            # print(type(value))

            time = datetime.now(UserTimeZone(time_zones_russia[time_zone]))
            time = str(time).split()[-1].split(':')
            user_time = float(f'{time[0]}.{time[1]}')
            good_morning = wakeup + 1

            if sleep >= 0 and sleep < 12:  # смотри сюда Иван!!!!
                sleep += 24
                wakeup += 24
                user_time += 24

            if user_time > wakeup and user_time < sleep:
                bot.send_message(chat_id=message.chat.id, text=f'Пора выпить {value}мл воды, осталось {current}мл.')

            if user_time > sleep and current <= 0:
                bot.send_message(chat_id=message.chat.id, text=f'Сегодня вы употребили свою суточную норму'
                                                               f' воды, хорошая работа!')
                User.update_current_value(message)

            if user_time > sleep and current >= 0:
                bot.send_message(chat_id=message.chat.id, text=f'Сегодня вы употребили не достаточно воды.'
                                                               f' Ничего страшного! Завтра у вас всё получится!')
                User.update_current_value(message)

            if user_time <= good_morning  and user_time >= wakeup:
                bot.send_message(chat_id=message.chat.id, text=f'Доброе утро! '
                                                               f'Пора выпить {value}мл воды, осталось {current}мл.')
        tl.start()
        while True:
            try:
                time.sleep(5)
                bot_status = User.check_bot_status(message)
                if bot_status == 'off':
                    raise KeyboardInterrupt
            except KeyboardInterrupt:
                print(tl.jobs)
                tl.stop()
                print(tl.jobs)
                global status
                status = 'stop'
                print(status)
                break  # send message to user every hour
        # del tl

    if status == 'start':
        print(status)
        start()
    # else:
    #     global tl
    #     del tl