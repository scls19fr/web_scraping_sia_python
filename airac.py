import datetime


AIRAC_INTERVAL = datetime.timedelta(days=28)
AIRAC_INITIAL_DATE = datetime.date(2015, 1, 8)


def airac_date(dt=None):
    if dt is None:
        dt = datetime.datetime.utcnow().date()
    return (
        AIRAC_INITIAL_DATE
        + ((dt - AIRAC_INITIAL_DATE).days // AIRAC_INTERVAL.days) * AIRAC_INTERVAL
    )
