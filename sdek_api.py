import json
import requests
import schedule

url = 'https://api.edu.cdek.ru/v2/calculator/tariff'


def update_token():
    with open('config.txt', 'r') as c:
        access_token = c.readline().strip('\n')


def get_token():
    url2 = 'https://api.edu.cdek.ru/v2/oauth/token?parameters'
    par = {'grant_type': 'client_credentials', 'client_id': 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
           'client_secret': 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'}
    request = requests.post(url2, params=par)
    with open('config.txt', 'r+') as c:
        c.truncate(0)
        c.seek(0)
        c.write(request.json()['access_token'])
    return


schedule.every(50).minutes.do(get_token)


data = json.dumps({
    "type": "2",
    "currency": "1",
    "tariff_code": "11",
    "from_location": {
        "code": 270
    },
    "to_location": {
        "code": 44
    },
    "services": [
        {
            "code": "CARTON_BOX_XS",
            "parameter": "2"
        }
    ],
    "packages": [
        {
            "height": 10,
            "length": 10,
            "weight": 4000,
            "width": 10
        }
    ]
})


header = {"Authorization": f"Bearer {access_token}", 'Content-Type': 'application/json'}
out = requests.post(url, data=data, headers=header)
print(out.content)

while True:
    schedule.run_pending()
