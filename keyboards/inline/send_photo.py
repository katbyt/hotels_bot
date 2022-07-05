from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.log_info import my_logger


def send_photo() -> InlineKeyboardMarkup:
    my_logger.debug('Создание инлайн-клавиатуры для уточнения демонстрации фотографий.')
    keyboard = InlineKeyboardMarkup()
    key_yes = InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.row(key_yes, key_no)
    return keyboard
