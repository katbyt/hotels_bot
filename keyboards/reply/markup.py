from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config_data.log_info import my_logger


def start_markup() -> ReplyKeyboardMarkup:
    my_logger.info('Создание кнопок с базовыми командами: "start" и "help".')
    markup = ReplyKeyboardMarkup(True, True)
    item_1 = KeyboardButton('/start')
    item_2 = KeyboardButton('/help')
    markup.row(item_1, item_2)
    return markup
