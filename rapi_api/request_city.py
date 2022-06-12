import json
from config_data.config import RAPID_API_KEY
from rapi_api.rapidapi import request_to_api


def city_founding(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }
    querystring = {"query": city, "locale": "ru_RU", "currency": "USD"}

    response = request_to_api(url, headers, querystring)

    if isinstance(response, str):
        return 'Что-то пошло не так...\nПовторите попытку позже!..'

    else:
        data = json.loads(response.text)

        # with open('test_city.json', 'w') as file:
        #     json.dump(data, file, indent=4)

        cities = list()
        if data.get('suggestions'):
            if data['suggestions'][0].get('entities'):

                for dest_id in data['suggestions'][0]['entities']:
                    cities.append({'city_name': dest_id['name'], 'destination_id': dest_id['destinationId']})

                return cities

        else:
            return 'Что-то пошло не так...\nПовторите попытку позже!..'
