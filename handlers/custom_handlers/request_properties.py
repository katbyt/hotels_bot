import json
from config_data.config import RAPID_API_KEY
from handlers.custom_handlers.rapidapi import request_to_api


def request_properties(dest_id, check_in, check_out, number):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": RAPID_API_KEY
    }
    querystring = {"destinationId": dest_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                   "checkOut": check_out, "adults1": "1", "sortOrder": "PRICE", "locale": "en_En", "currency": "USD"}

    response = request_to_api(url, headers, querystring)
    data = json.loads(response.text)

    properties = list()
    for i in data['data']['body']['searchResults']['results']:
        if len(properties) < int(number):
            properties.append({'id': i['id'], 'name': i['name'],
                               'address': f"{i['address']['streetAddress']}, {i['address']['locality']}",
                               'distance': i['landmarks'][0]['distance'],
                               'price': i['ratePlan']['price']['current'],
                               'url': f"https://hotels.com/ho{i['id']}"})

    return properties
