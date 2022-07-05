import json
from config_data.config import RAPID_API_KEY
from rapi_api.rapidapi import request_to_api
from config_data.log_info import my_logger


def city_founding(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }
    querystring = {"query": city, "locale": "ru_RU", "currency": "USD"}

    my_logger.debug('Попытка запроса к API для поиска города.')
    response = request_to_api(url, headers, querystring)

    if isinstance(response, str):
        my_logger.warning('Нет ответа от API.')
        return 'Что-то пошло не так...\nПовторите попытку позже!..'

    else:
        my_logger.debug('Возврат ответа от API.')
        data = json.loads(response.text)

        # with open('test_city.json', 'w') as file:
        #     json.dump(data, file, indent=4)

        cities = list()
        if data.get('suggestions'):
            if data['suggestions'][0].get('entities'):
                my_logger.debug('Формирование списка городов для продолжения сценария.')

                for dest_id in data['suggestions'][0]['entities']:
                    cities.append({'city_name': dest_id['name'], 'destination_id': dest_id['destinationId']})

                return cities

        else:
            my_logger.warning('Некорректный формат данных, полученных от API.')
            return 'Что-то пошло не так...\nПовторите попытку позже!..'
