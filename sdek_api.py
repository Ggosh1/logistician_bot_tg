import requests
import datetime
from config import SDEK_CODES
time_now = str(datetime.datetime.now())
time_formatted = time_now[:10] + "T" + time_now[11:19] + "+0300"


def get_token():
    with open('config.txt', 'r') as c:
        sdek_access_token = c.readline().strip('\n')
        return sdek_access_token


def update_token():
    url2 = 'https://api.edu.cdek.ru/v2/oauth/token?parameters'
    par = {'grant_type': 'client_credentials', 'client_id': 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
           'client_secret': 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'}
    request = requests.post(url2, params=par)
    with open('config.txt', 'r+') as c:
        c.truncate(0)
        c.seek(0)
        c.write(request.json()['access_token'])
    return


def get_city_code(city):
    return SDEK_CODES[city]


def get_info_delivery(from_location, to_location, height, width, length, weight, amount):
    calculator_url = 'https://api.edu.cdek.ru/v2/calculator/tarifflist'
    packages = [{"height": height, "length": length, "weight": weight, "width": width} for _ in range(amount)]
    try:
        code_from_location = get_city_code(from_location)
        code_to_location = get_city_code(to_location)
    except KeyError:
        return f'Доставки в город {to_location}, либо доставки из города {from_location} нет'
    j = {
        "type": 2,
        "currency": 1,
        "from_location": {
            "code": code_from_location
        },
        "to_location": {
            "code": code_to_location
        },
        "packages": packages
    }
    print(j)
    return requests.post(url=calculator_url, json=j, headers={"Authorization": f"Bearer {get_token()}"}).json()
