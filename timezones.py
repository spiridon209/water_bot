from datetime import tzinfo, timedelta, datetime

time_zones_russia = {'UTC+2': 7200, 'UTC+3': 10800, 'UTC+4': 14400, 'UTC+5': 18000,
                     'UTC+6': 21600, 'UTC+7': 25200, 'UTC+8': 28800, 'UTC+9': 32400,
                     'UTC+10': 36000, 'UTC+11': 39600, 'UTC+12': 43200}


class UserTimeZone(tzinfo):

    def __init__(self, offset=10800, name=None):
        self.offset = timedelta(seconds=offset)
        self.name = name or self.__class__.__name__

    def utcoffset(self, dt):
        return self.offset

    def tzname(self, dt):
        return self.name

    def dst(self, dt):
        return timedelta(0)


def get_user_current_time_utc(user_time_zone):
    time_utc = datetime.now(UserTimeZone(user_time_zone))
    print(str(time_utc))  #
    float_time = str(time_utc).split()[-1].split(':')  # НАПИСАТЬ ФУНКЦИЮ
    print(float_time)
    user_time = float(f'{float_time[0]}.{float_time[1]}')
    return user_time
