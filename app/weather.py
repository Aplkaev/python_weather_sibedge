import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from dotenv import load_dotenv, dotenv_values

from app.db.WetherModel import Weather, database

headers = {
    'Cookie': 'autocity=4588; selector_args=%7B%22region%22%3A%22477%22%2C%22country%22%3A%22156%22%2C%22distr%22%3A%22298%22%2C%22city%22%3A%224652%22%2C%22month%22%3Anull%2C%22year%22%3Anull%7D',
    "User-Agent": "Firefox/3.5.8"
}

async def bs4_parser(response, number_month):
    soup = BeautifulSoup(response.text, 'html.parser')

    for tr in soup.find_all('tr'):
        td_number_day = tr.find('td', class_='first')
        td_temperature = tr.find('td', class_='first_in_group')
        if td_number_day is None or td_temperature.find('img') is not None:
            continue

        current_dateTime = datetime(2018, number_month,
                                    int(td_number_day.text), 12, 00)
        await Weather.objects.get_or_create(
            date=current_dateTime,
            temperature=int(td_temperature.text))


async def load_months():
    config = dotenv_values()
    url_weather = config['URL_WEATHER']
    len_months = int(config['LEN_MONTHS'])
    print('start load weahter')
    for i in range(1, len_months + 1):
        # TODO env
        url = url_weather + str(i)
        print('load {} month url:{}'.format(i, url))
        response = requests.request("GET", url, headers=headers)
        await bs4_parser(response, i)
        time.sleep(5)

if __name__ == '__main__':
    load_dotenv()
    if not database.is_connected:
        database.connect()
    current_dateTime = datetime.now()
    load_months()
