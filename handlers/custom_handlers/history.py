from loader import bot
from telebot.types import Message
from database.hotels_db import User, db
from config_data.log_info import my_logger


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    my_logger.debug(f'Пользователь {message.from_user.id} выбрал команду: {message.text}')
    with db:
        my_logger.debug('Проверка наличия пользователя в базе данных.')
        check_history = User.select().where(User.user_id == message.from_user.id)
    if check_history:
        my_logger.debug('Пользователь найден в базе данных. Формирование и отправка результата.')
        if len(check_history) > 5:
            check_history = check_history[-5:]
            bot.send_message(message.from_user.id, 'Демонстрация не более 5 последних полученных результатов:')
        for result in check_history:
            bot.send_message(message.from_user.id, f'Пользователь: {message.from_user.full_name}\n'
                                                   f'Команда: {result.command}\n'
                                                   f'Дата и время запроса: {result.created_date}\n\n'
                                                   f'Результат поиска: \n{result.history}',
                             disable_web_page_preview=True)
    else:
        my_logger.debug('Пользователь не найден в базе данных. Вывод соответствующего уведомления.')
        bot.send_message(message.from_user.id, f'У пользователя - {message.from_user.full_name} - нет истории поиска.')
