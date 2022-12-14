import json
from config_data.config import RAPID_API_KEY
from rapi_api.rapidapi import request_to_api
from config_data.log_info import my_logger


def request_properties(dest_id, check_in, check_out, number, price_min, price_max, distance, sort_order):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": RAPID_API_KEY
    }
    querystring = {"destinationId": dest_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                   "checkOut": check_out, "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                   "sortOrder": sort_order, "locale": "ru_RU", "currency": "USD", "landmarkIds": "City center"}

    my_logger.debug('Попытка запроса к API для получения характеристик отеля.')
    response = request_to_api(url, headers, querystring)

    if isinstance(response, str):
        my_logger.warning('Нет ответа от API.')
        return 'Что-то пошло не так...\nПовторите попытку позже!..'

    else:
        my_logger.debug('Возврат ответа от API.')
        data = json.loads(response.text)

        # with open('test_prop.json', 'w') as file:
        #     json.dump(data, file, indent=4)

        properties = list()
        data_list = data.get('data', {}).get('body', {}).get('searchResults', {}).get('results')
        if data_list:
            my_logger.debug('Формирование характеристик отеля для продолжения сценария.')
            for i in data_list:
                if len(properties) < int(number):
                    if distance[0] < float(i.get('landmarks')[0].get('distance')[:-3].replace(',', '.')) < distance[1]:
                        properties.append({'id': i.get('id'), 'name': i.get('name'),
                                           'address': f"{i.get('address').get('streetAddress', '')}, "
                                                      f"{i.get('address').get('locality')}",
                                           'distance': i.get('landmarks')[0].get('distance'),
                                           'price': i.get('ratePlan', {}).get('price', {}).get('current', 0),
                                           'url': f"https://hotels.com/ho{i['id']}"})
                else:
                    return properties

        else:
            my_logger.warning('Некорректный формат данных, полученных от API.')
            return 'Что-то пошло не так...\nПовторите попытку позже!..'
