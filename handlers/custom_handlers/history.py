from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Здесь будет команда /history')
