import calendar
from datetime import datetime


def timestamp_to_datetime(ts):
    return datetime.utcfromtimestamp(float(ts))


def datetime_to_timestamp(dt):
    return calendar.timegm(dt.timetuple())

def datetime_to_django(dt):
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
