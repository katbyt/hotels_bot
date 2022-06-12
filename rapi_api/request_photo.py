import json
from config_data.config import RAPID_API_KEY
from rapi_api.rapidapi import request_to_api
import random


def request_photo(number, hotel_id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }
    querystring = {"id": hotel_id}

    response = request_to_api(url, headers, querystring)

    if isinstance(response, str):
        return 'Что-то пошло не так...\nПовторите попытку позже!..'

    else:
        data = json.loads(response.text)

        # with open('test_photo.json', 'w') as file:
        #     json.dump(data, file, indent=4)

        photo_list = []
        for elem in (random.choice(data.get('hotelImages')) for _ in range(int(number))):
            photo_list.append(elem['baseUrl'].replace('_{size}', ''))

        return photo_list
