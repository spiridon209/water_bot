
import time
from datetime import timedelta, datetime
from timeloop import Timeloop

from user import User
from timezones import UserTimeZone, time_zones_russia

def send_message_per_hour(bot):
    tl = Timeloop()

    @tl.job(interval=timedelta(seconds=15))
    def send_message():
        pass


