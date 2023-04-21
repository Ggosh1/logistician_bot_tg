import requests
import json


def get_zip_index(token, city):
    data = json.loads(bytes(requests.get(
        f'https://api.boxberry.ru/json.php?token={token}&method=ListZips').content).decode(
        'utf-8'))
    for i in data:
        if i['City'] == city:
            return i['Zip']


def get_pvz_code(token, city):
    data = json.loads(bytes(requests.get(f'https://api.boxberry.ru/json.php?token={token}&method=ListPoints').content).decode('utf-8'))
    for i in data:
        if i['CityName'] == city:
            return i['Code']

def get_info_delivery(token, weight, city_from, city_to, height, width, depth, is_target):
    url = f'https://api.boxberry.ru/json.php?token={token}&method=DeliveryCosts'
    targetstart = get_pvz_code(token, city_from)
    params = {'token': token, 'weight': weight, 'targetstart': targetstart}
    if is_target:
        target_or_zip_code = get_pvz_code(token, city_to)
        params['target'] = target_or_zip_code
    else:
        target_or_zip_code = get_zip_index(token, city_to)
        params['zip'] = target_or_zip_code
    params['ordersum'] = 0
    params['height'] = height
    params['width'] = width
    params['depth'] = depth
    return json.loads(bytes(requests.get(url, params=params).content).decode('utf-8'))




#print(get_info_delivery(token='d6f33e419c16131e5325cbd84d5d6000', weight=5, city_from='Москва', city_to='Чита', height=0.6, width=1, depth=1, is_target=True))