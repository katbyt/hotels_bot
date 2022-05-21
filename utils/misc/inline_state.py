from telebot.handler_backends import State
from telebot.custom_filters import StateFilter
from telebot.types import Message, CallbackQuery


class UpdateStateFilter(StateFilter):
    def check(self, message, text):
        if text == '*':
            return True

        chat_id, user_id = None, None

        if isinstance(message, Message):  # Вытягиваем нужное если сработал "message_handler"
            chat_id = message.chat.id
            user_id = message.from_user.id

        if isinstance(message, CallbackQuery):  # Вытягиваем нужное если сработал "callback_query_handler"
            chat_id = message.message.chat.id
            user_id = message.from_user.id
            message = message.message

        if isinstance(text, list):
            new_text = []
            for i in text:
                if isinstance(i, State):
                    new_text.append(i)
            text = new_text

        if message.chat.type == 'group':
            group_state = self.bot.current_states.get_state(user_id, chat_id)
            if group_state == text:
                return True
            elif group_state in text and type(text) is list:
                return True

        else:
            user_state = self.bot.current_states.get_state(user_id, chat_id)
            if user_state == text:
                return True
            elif type(text) is list and user_state in text:
                return True
