from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from utils.misc.inline_state import UpdateStateFilter

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(UpdateStateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
