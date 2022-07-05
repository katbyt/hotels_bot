from telebot.types import ReplyKeyboardMarkup
from config_data.log_info import my_logger


def farther() -> ReplyKeyboardMarkup:
    my_logger.debug('Создание вспомогательной кнопки "Дальше".')
    markup = ReplyKeyboardMarkup(True)
    markup.add('Дальше')
    return markup
