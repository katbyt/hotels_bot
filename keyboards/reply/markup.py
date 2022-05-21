from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(True, True)
    item_1 = KeyboardButton('/start')
    item_2 = KeyboardButton('/help')
    markup.row(item_1, item_2)
    return markup
