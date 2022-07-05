from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from utils.misc.inline_state import UpdateStateFilter
from config_data.log_info import my_logger

if __name__ == '__main__':
    my_logger.info('Запуск бота.')
    bot.add_custom_filter(UpdateStateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
