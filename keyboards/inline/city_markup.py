from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.custom_handlers.city_founding import city_founding


def city_markup(city):
    cities = city_founding(city)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'],
                                              callback_data=f'{city["destination_id"]}'))
    return destinations
