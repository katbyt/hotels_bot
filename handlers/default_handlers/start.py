from telebot.types import Message
from loader import bot
from keyboards.reply.markup import start_markup


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.chat.id, 'Вас приветствует телеграм-бот для поиска отелей!\n'
                                      'Для продолжения работы нажмите /help.', reply_markup=start_markup())
