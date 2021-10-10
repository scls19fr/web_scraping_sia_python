import click
import datetime
from airac import airac_date
from sia import BASE_URL_SIA, format_french_date
from pathlib import Path
import requests


def download_sia_vac(code):
    dt = datetime.datetime.utcnow()
    dt_airac = airac_date(dt.date())
    path = Path(__file__).parent / dt_airac.isoformat()
    path.mkdir(parents=True, exist_ok=True)

    airac_string = format_french_date(dt_airac)
    endpoint = "/dvd/eAIP_%s/Atlas-VAC/PDF_AIPparSSection/VAC/AD/AD-2.%s.pdf" % (airac_string, code)
    url = BASE_URL_SIA + endpoint
    print(" from %s" % url)

    r = requests.get(url)
    with open(path / ("AD-2.%s.pdf" % code), 'wb') as f:
        f.write(r.content)

@click.command()
@click.argument(
    "code",
)
def main(code):
    """Download VAC from SIA."""
    codes = code.split(",")
    for code in codes:
        print("Downloading VAC for %s" % code)
        download_sia_vac(code)

    print("end of downloading VAC")


if __name__ == "__main__":
    main()
