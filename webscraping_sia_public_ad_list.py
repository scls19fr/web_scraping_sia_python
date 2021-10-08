import click
import datetime
from selenium import webdriver
from time import sleep
import pandas as pd


# AIRAC
AIRAC_INTERVAL = datetime.timedelta(days=28)
AIRAC_INITIAL_DATE = datetime.date(2015, 1, 8)

def airac_date(dt = None):
    if dt is None:
        dt = datetime.datetime.utcnow().date()
    return AIRAC_INITIAL_DATE + ((dt - AIRAC_INITIAL_DATE).days // AIRAC_INTERVAL.days) * AIRAC_INTERVAL


# SIA
BASE_URL_SIA = "https://www.sia.aviation-civile.gouv.fr"
MONTH_FR = ['', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

def format_french_date(dt):
    return "%02d_%s_%d" % (dt.day, MONTH_FR[dt.month], dt.year)


def webscrap_sia(driver, dt, username, password):
    base_url = BASE_URL_SIA

    dt_airac = airac_date(dt.date())
    # airac_string = "07_OCT_2021"
    airac_string = format_french_date(dt_airac)

    base_url = BASE_URL_SIA
    endpoint = "/dvd/eAIP_%s/Atlas-VAC/FR/VACProduitPartie.htm" % airac_string
    url = base_url + endpoint
    driver.get(url)
    assert "Untitled Document" in driver.title

    xpath = "/html/body/form/b/b/b/b/select"
    element = driver.find_element_by_xpath(xpath)

    codes = []
    names = []
    for opt in element.find_elements_by_tag_name("option"):
        codes.append(opt.get_property("value"))
        names.append(opt.text)

    df = pd.DataFrame({"code": codes, "name": names})

    iso_date = dt_airac.isoformat()
    fname = "AD_%s.xlsx" % iso_date
    print("Write %s" % fname)
    df.to_excel(fname, index=False)

    fname = "AD_%s.csv" % iso_date
    print("Write %s" % fname)
    df.to_csv(fname, index=False, sep=";")


@click.command()
@click.option(
    "--driver",
    default="chrome",
    help="Selenium web driver ('chrome', 'firefox' (aka 'gecko')",
)
@click.option(
    "--username", default="", help="username",
)
@click.option(
    "--password", default="", help="password",
)
def main(driver, username, password):
    """Web scraping SIA data."""
    # if username == "" or password == "":
    #    raise ValueError("--username USERNAME --password PASSWORD sont requis")

    driver = driver.lower()

    if driver in ["firefox", "gecko"]:
        driver = webdriver.Firefox()
    elif driver == "chrome":
        driver = webdriver.Chrome()
    else:
        raise NotImplementedError(f"unsupported web driver {driver}")

    dt = datetime.datetime.utcnow()

    webscrap_sia(driver, dt, username, password)

    sleep(1)

    driver.quit()

    print("end of scraping")


if __name__ == "__main__":
    main()