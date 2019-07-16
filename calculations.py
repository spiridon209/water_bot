def get_male_amount(weight):
    answer = weight * 35
    return answer


def get_female_amount(weight):
    answer = weight * 31
    return answer


def get_water_volume_per_hour(wake_up_time, sleep_time, daily_value_of_water):
    if wake_up_time < sleep_time:
        waking_hours = sleep_time - wake_up_time
    else:
        waking_hours = 24 - (wake_up_time - sleep_time)

    return int(daily_value_of_water/waking_hours)
