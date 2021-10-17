from airac import airac_date


BASE_URL_SIA = "https://www.sia.aviation-civile.gouv.fr"
MONTH_FR = [
    "",
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
]


def format_french_date(dt):
    return "%02d_%s_%02d" % (dt.day, MONTH_FR[dt.month], dt.year)
