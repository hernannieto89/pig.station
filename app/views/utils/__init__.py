import time


def check_minutes_passed(oldepoch, minutes=1):
    return time.time() - oldepoch >= 60*minutes
