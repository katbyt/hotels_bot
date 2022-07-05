from telebot.types import Message
from loader import bot
from keyboards.reply.markup import start_markup
from config_data.log_info import my_logger


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    my_logger.info(f'Команда: {message.text}')
    bot.send_message(message.chat.id, 'Вас приветствует телеграм-бот для поиска отелей!\n'
                                      'Для продолжения работы нажмите /help.', reply_markup=start_markup())
