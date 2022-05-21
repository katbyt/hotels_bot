from telebot.types import Message
from handlers.default_handlers import help
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    help.bot_help(message)
