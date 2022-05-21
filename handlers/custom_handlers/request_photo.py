import json
from config_data.config import RAPID_API_KEY
from handlers.custom_handlers.rapidapi import request_to_api
import random


def request_photo(number, hotel_id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }
    querystring = {"id": hotel_id}

    response = request_to_api(url, headers, querystring)
    data = json.loads(response.text)

    photo_list = []
    for elem in (random.choice(data['hotelImages']) for _ in range(int(number))):
        photo_list.append(elem['baseUrl'].format(size='z'))

    return photo_list
