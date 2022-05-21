from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    command = State()
    city = State()
    dest_id = State()
    check_in = State()
    check_out = State()
    price = State()
    distance = State()
    hotels_count = State()
    photo = State()
    photos_count = State()
    result = State()
