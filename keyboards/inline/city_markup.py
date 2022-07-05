from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from rapi_api.request_city import city_founding
from config_data.log_info import my_logger


def city_markup(city):
    my_logger.debug('Попытка формирования списка городов.')
    cities = city_founding(city)

    if isinstance(cities, list):
        my_logger.debug('Создание инлайн-клавиатуры для уточнения локации.')
        destinations = InlineKeyboardMarkup()
        for city in cities:
            destinations.add(InlineKeyboardButton(text=city['city_name'],
                                                  callback_data=f'{city["destination_id"]}'))
        return destinations

    else:
        my_logger.warning('Некорректный формат данных, полученных от API.')
        return 'Что-то пошло не так...\nПовторите попытку позже!..'
