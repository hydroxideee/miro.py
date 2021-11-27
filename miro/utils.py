import datetime


def parse_date(datetimestr: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.strptime(datetimestr, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return None

