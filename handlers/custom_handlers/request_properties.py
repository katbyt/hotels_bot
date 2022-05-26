import json
from config_data.config import RAPID_API_KEY
from handlers.custom_handlers.rapidapi import request_to_api


def request_properties(dest_id, check_in, check_out, number, price_min, price_max, distance, sort_order):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": RAPID_API_KEY
    }
    querystring = {"destinationId": dest_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                   "checkOut": check_out, "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                   "sortOrder": sort_order, "locale": "ru_RU", "currency": "USD"}

    response = request_to_api(url, headers, querystring)
    data = json.loads(response.text)

    # with open('test_prop.json', 'w') as file:
    #     json.dump(data, file, indent=4)

    properties = list()
    for i in data['data']['body']['searchResults']['results']:
        if len(properties) < int(number):
            if distance[0] < i['landmarks'][0]['distance'][:-3] < distance[1]:
                properties.append({'id': i['id'], 'name': i['name'],
                                   'address': f"{i['address'].get('streetAddress', '')}, {i['address']['locality']}",
                                   'distance': i['landmarks'][0]['distance'],
                                   'price': i.get('ratePlan', {}).get('price', {}).get('current', 0),
                                   'url': f"https://hotels.com/ho{i['id']}"})
    return properties
