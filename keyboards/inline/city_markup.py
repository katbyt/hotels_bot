from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from rapi_api.request_city import city_founding


def city_markup(city):
    cities = city_founding(city)

    if isinstance(cities, list):
        destinations = InlineKeyboardMarkup()
        for city in cities:
            destinations.add(InlineKeyboardButton(text=city['city_name'],
                                                  callback_data=f'{city["destination_id"]}'))
        return destinations

    else:
        return 'Что-то пошло не так...\nПовторите попытку позже!..'
