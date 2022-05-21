import json
from config_data.config import RAPID_API_KEY
from handlers.custom_handlers.rapidapi import request_to_api


def city_founding(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }
    querystring = {"query": city, "locale": "en_En", "currency": "USD"}

    response = request_to_api(url, headers, querystring)
    data = json.loads(response.text)

    cities = list()
    for dest_id in data['suggestions'][0]['entities']:
        cities.append({'city_name': dest_id['name'], 'destination_id': dest_id['destinationId']})
    return cities
