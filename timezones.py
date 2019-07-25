from datetime import datetime, timezone


def get_user_utc_0(user_tz, wake_up, sleep):

    time_zones_russia = {'UTC+2': 2, 'UTC+3': 3, 'UTC+4': 4, 'UTC+5': 5,
                         'UTC+6': 6, 'UTC+7': 7, 'UTC+8': 8, 'UTC+9': 9,
                         'UTC+10': 10, 'UTC+11': 11, 'UTC+12': 12}

    wake_up -= time_zones_russia[user_tz]
    sleep -= time_zones_russia[user_tz]
    return wake_up, sleep


if __name__ == '__main__':
    a = datetime.now(timezone.utc)
    print(a)