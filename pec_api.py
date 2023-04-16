import requests
import json
import string


class NoDeliveryToThisCity(Exception):
    pass


def get_city_code(city):
    town_list_url = 'http://www.pecom.ru/ru/calc/towns.php'
    town_list = json.loads(bytes(requests.get(town_list_url).content).decode('utf-8'))
    #print(town_list) #
    # TODO: тут баг с москвой как минимум, пэк почему то написали Москва Восток, возможны баги с другими городами
    if city.lower().capitalize() in town_list.keys():
        return list(town_list[city.lower().capitalize()].keys())[0] # TODO: пока что тупо берет первый район
    return False


def get_info_delivery(city_from: string, city_to: string, weight: int, width: int, long: int,
                    height: int, volume: int, is_gabarit=True, need_protected_package=False, places=1):
    calculator_url = 'http://calc.pecom.ru/bitrix/components/pecom/calc/ajax.php'
    code_city_from = get_city_code(city_from)
    code_city_to = get_city_code(city_to)
    if code_city_from and code_city_to:
        params = {}
        for i in range(places):  # в основном скрипте нужно проверить, что введенное количество мест преобразуется в int
            params[f'places[{i}]'] = [width, long, height, volume, weight, is_gabarit, need_protected_package]
        params[f'take[town]'] = code_city_from
        params[f'deliver[town]'] = code_city_to
        return json.loads(bytes(requests.get(calculator_url, params=params).content).decode('utf-8'))
    else:
        raise NoDeliveryToThisCity

