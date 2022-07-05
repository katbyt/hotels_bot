from loader import bot
from states.user_info import UserInfoState
from telebot.types import Message
from config_data.log_info import my_logger


@bot.message_handler(state=UserInfoState.price)
def get_price(message: Message) -> None:
    if [item.isdigit() for item in message.text.split()] == [True, True]:
        my_logger.debug('Сохранение диапазона цен. Запрос диапазона расстояния.')
        bot.set_state(message.from_user.id, UserInfoState.distance, message.chat.id)
        bot.send_message(message.from_user.id, "Укажите удаленность от центра в км (диaпазон через пробел)!")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price'] = sorted(list(map(int, message.text.split())))
    else:
        my_logger.warning('Указаны некорректные данные.')
        bot.send_message(message.from_user.id, 'Укажите, пожалуйста, корректную информацию!')


@bot.message_handler(state=UserInfoState.distance)
def get_distance(message: Message) -> None:
    if [item.isdigit() for item in message.text.split()] == [True, True]:
        my_logger.debug('Сохранение диапазона расстояния. Запрос количества отелей.')
        bot.set_state(message.from_user.id, UserInfoState.hotels_count, message.chat.id)
        bot.send_message(message.from_user.id, "Укажите количество отелей! (не более 5)")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance'] = sorted(list(map(int, message.text.split())))
    else:
        my_logger.warning('Указаны некорректные данные.')
        bot.send_message(message.from_user.id, 'Укажите, пожалуйста, корректную информацию!')
