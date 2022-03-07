import requests
from bs4 import BeautifulSoup

from no_power_email import send_no_power_email


def main():
    split_no_power_data = {}

    res = requests.get(
        "https://www.hep.hr/ods/bez-struje/19?dp=split&el=208&datum=07.03.2022"
    )
    soup = BeautifulSoup(res.content, "html.parser")

    no_power_where_divs = soup.find_all("div", {"class": "mjesto tipR"})
    no_power_when_divs = soup.find_all("div", {"class": "vrijeme tipR"})

    if not no_power_where_divs:
        return

    for i, div in enumerate(no_power_where_divs):
        town = div.find("div", {"class": "grad"}, recursive=False)
        if town and "split" in town.text.lower():
            split_no_power_data["where"] = div.text
            split_no_power_data["when"] = find_no_power_hours(no_power_when_divs, i)

    send_no_power_email(split_no_power_data)


def find_no_power_hours(time_divs, split_index):
    for i, div in enumerate(time_divs):
        if i == split_index:
            return div.text


if __name__ == "__main__":
    main()
