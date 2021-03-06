import logging
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

from no_power_email import send_no_power_email

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    split_no_power_data = []
    split_hep_url = "https://www.hep.hr/ods/bez-struje/19?dp=split&el=208"
    tomorrow_date = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    final_url = split_hep_url + f"&datum={tomorrow_date}"

    logger.info("final_url: %s", final_url)

    res = requests.get(final_url)
    soup = BeautifulSoup(res.content, "html.parser")

    no_power_where_divs = soup.find_all("div", {"class": "mjesto tipR"})
    no_power_when_divs = soup.find_all("div", {"class": "vrijeme tipR"})

    if not no_power_where_divs:
        logger.info("no_power_where_divs_empty")
        return

    for i, div in enumerate(no_power_where_divs):
        town = div.find("div", {"class": "grad"}, recursive=False)
        if town and "split" in town.text.lower():
            split_no_power_data.append(
                {"where": div.text, "when": find_no_power_hours(no_power_when_divs, i)}
            )

    if split_no_power_data:
        logger.info("split_no_power_data_present")
        return send_no_power_email(tomorrow_date, split_no_power_data)

    logger.info("split_no_power_data_empty")


def find_no_power_hours(time_divs, split_index):
    for i, div in enumerate(time_divs):
        if i == split_index:
            return div.text
