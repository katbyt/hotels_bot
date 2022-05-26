from loader import bot
from states.user_info import UserInfoState
from telebot.types import Message


@bot.message_handler(state=UserInfoState.price)
def get_price(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.distance, message.chat.id)
    bot.send_message(message.from_user.id, "Укажите удаленность от центра в км (диaпазон через пробел)!")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price'] = map(int, message.text.split())


@bot.message_handler(state=UserInfoState.distance)
def get_distance(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.hotels_count, message.chat.id)
    bot.send_message(message.from_user.id, "Укажите количество отелей!")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['distance'] = message.text.split()