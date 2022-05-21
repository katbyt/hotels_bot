from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def send_photo() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    key_yes = InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.row(key_yes, key_no)
    return keyboard
