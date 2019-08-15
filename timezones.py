from datetime import datetime, timezone


def get_user_utc_0(user_tz, wake_up, sleep):

    time_zones_russia = {'UTC+2': 2, 'UTC+3': 3, 'UTC+4': 4, 'UTC+5': 5,
                         'UTC+6': 6, 'UTC+7': 7, 'UTC+8': 8, 'UTC+9': 9,
                         'UTC+10': 10, 'UTC+11': 11, 'UTC+12': 12}

    wake_up -= round(time_zones_russia[user_tz], 2)
    sleep -= round(time_zones_russia[user_tz], 2)

    if sleep < 0:
        sleep += 24

    if wake_up < 0:
        wake_up += 24

    return wake_up, sleep


def get_current_utc_time():
    return datetime.now(timezone.utc)
