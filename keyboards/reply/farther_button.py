from telebot.types import ReplyKeyboardMarkup


def farther() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(True)
    markup.add('Дальше')
    return markup
