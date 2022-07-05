from telebot.types import Message
from loader import bot
from config_data.log_info import my_logger


@bot.message_handler(state=None)
def bot_echo(message: Message):
    my_logger.warning(f'Введены некорректные данные (Команда: /echo)')
    bot.send_message(message.from_user.id, 'Следуйте, пожалуйста, рекомендациям бота!')
