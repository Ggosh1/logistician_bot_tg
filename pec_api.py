import requests
import json
import string


class NoDeliveryToThisCity(Exception):
    pass


def get_city_code(city):
    town_list_url = 'http://www.pecom.ru/ru/calc/towns.php'
    town_list = json.loads(bytes(requests.get(town_list_url).content).decode('utf-8'))
    #print(town_list) #
    #print(city)
    # TODO: тут баг с москвой как минимум, пэк почему то написали Москва Восток, возможны баги с другими городами
    if city.lower() == 'москва':
        return '-446'
    if city in town_list.keys():
        return list(town_list[city].keys())[0] # пока что тупо берет первый район
    return False


def get_info_delivery(city_from: string, city_to: string, weight: int, width: int, long: int,
                    height: int, volume: int, is_negabarit=False, need_protected_package=False, places=1):
    calculator_url = 'http://calc.pecom.ru/bitrix/components/pecom/calc/ajax.php'
    code_city_from = get_city_code(city_from)
    code_city_to = get_city_code(city_to)
    if code_city_from and code_city_to:
        params = {}
        for i in range(places):  # в основном скрипте нужно проверить, что введенное количество мест преобразуется в int
            params[f'places[{i}]'] = [width, long, height, volume, weight, is_negabarit, need_protected_package]
        params[f'take[town]'] = code_city_from
        params[f'deliver[town]'] = code_city_to
        params['take[tent]'] = 0
        params['take[gidro]'] = 0
        params['take[manip]'] = 0
        params['take[speed]'] = 0
        params['deliver[tent]'] = 0
        params['deliver[gidro]'] = 0
        params['deliver[manip]'] = 0
        params['deliver[speed]'] = 0
        params['plombir'] = 0
        params['strah'] = 0
        params['ashan'] = 0
        params['night'] = 0
        params['pal'] = 0
        params['pallets'] = 0
        print(params)
        return json.loads(bytes(requests.get(calculator_url, params=params).content).decode('utf-8'))
    else:
        raise NoDeliveryToThisCity


