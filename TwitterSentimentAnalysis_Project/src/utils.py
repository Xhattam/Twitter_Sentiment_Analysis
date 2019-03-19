from datetime import datetime


def get_timestamp():
    now = datetime.now()
    return "{}{}{}_{}:{}".format(now.day, now.month, now.year, now.hour, now.minute)

