import datetime


def parse_date(datetimestr: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.strptime(datetimestr, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return None

