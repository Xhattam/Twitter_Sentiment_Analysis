from datetime import datetime


def get_timestamp():
    now = datetime.now()
    return "{}/{}/{}_{}h{}".format(now.day, now.month, now.year, now.hour, now.minute)

