from loader import bot
from telebot.types import Message
from states.user_info import UserInfoState


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите город для поиска!')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
