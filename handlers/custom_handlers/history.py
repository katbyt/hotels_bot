from loader import bot
from telebot.types import Message
from database.hotels_db import User


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    if User.select().where(User.user_id == message.from_user.id):
        for result in User.select().where(User.user_id == message.from_user.id):
            bot.send_message(message.from_user.id, f'Пользователь: {message.from_user.full_name}\n'
                                                   f'Команда: {result.command}\n'
                                                   f'Дата и время запроса: {result.created_date}\n\n'
                                                   f'Результат поиска: \n{result.history}',
                             disable_web_page_preview=True)
    else:
        bot.send_message(message.from_user.id, f'У пользователя - {message.from_user.full_name} - нет истории поиска.')
