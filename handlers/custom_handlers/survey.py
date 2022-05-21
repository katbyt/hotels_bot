from loader import bot
from states.user_info import UserInfoState
from telebot.types import Message, CallbackQuery, InputMediaPhoto
from handlers.custom_handlers.calendar import get_calendar
from keyboards.inline.send_photo import send_photo
from keyboards.inline.city_markup import city_markup
from keyboards.reply.farther_button import farther
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta
from keyboards.reply.markup import start_markup
from handlers.custom_handlers.request_photo import request_photo
from handlers.custom_handlers.request_properties import request_properties


@bot.message_handler(state=UserInfoState.city)
def city_search(message):
    bot.set_state(message.from_user.id, UserInfoState.dest_id, message.chat.id)
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:',
                     reply_markup=city_markup(message.text))

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.callback_query_handler(func=None, state=UserInfoState.dest_id)
def get_check_in(call: CallbackQuery) -> None:
    ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}

    bot.answer_callback_query(call.id, text='Город выбран!')
    bot.edit_message_text("Выберите дату заезда!", call.message.chat.id, call.message.message_id)

    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['dest_id'] = call.data

    today = date.today()
    calendar, step = get_calendar(calendar_id=1,
                                  current_date=today,
                                  min_date=today,
                                  max_date=today + timedelta(days=365),
                                  locale="ru")

    bot.set_state(call.message.chat.id, UserInfoState.check_in, call.message.chat.id)
    bot.send_message(call.message.chat.id, f"Выберите {ALL_STEPS[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def handle_arrival_date(call: CallbackQuery):
    ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}

    today = date.today()
    result, key, step = get_calendar(calendar_id=1,
                                     current_date=today,
                                     min_date=today,
                                     max_date=today + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_in'] = result

            bot.edit_message_text(f"Дата заезда {result}",
                                  call.message.chat.id,
                                  call.message.message_id)

            bot.send_message(call.from_user.id, "Выберите дату выезда!")
            calendar, step = get_calendar(calendar_id=2,
                                          min_date=data['check_in'],
                                          max_date=data['check_in'] + timedelta(days=365),
                                          locale="ru",
                                          )

            bot.send_message(call.from_user.id,
                             f"Выберите {ALL_STEPS[step]}",
                             reply_markup=calendar)

            bot.set_state(call.from_user.id, UserInfoState.check_out, call.message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def handle_departure_date(call: CallbackQuery):
    ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data_check_in = data['check_in']

    result, key, step = get_calendar(calendar_id=2,
                                     min_date=data_check_in,
                                     max_date=data_check_in + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_out'] = result
            data['count_days'] = (data['check_out'] - data['check_in']).days + 1

            bot.edit_message_text(f"Дата выезда {result}",
                                  call.message.chat.id,
                                  call.message.message_id)

            if data['command'] == '/bestdeal':
                bot.set_state(call.from_user.id, UserInfoState.price, call.message.chat.id)
                bot.send_message(call.message.chat.id, "Укажите диaпазон цен (через пробел)!")

            else:
                bot.set_state(call.from_user.id, UserInfoState.hotels_count, call.message.chat.id)
                bot.send_message(call.message.chat.id, "Укажите количество отелей!")


@bot.message_handler(state=UserInfoState.price)
def get_price(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.distance, message.chat.id)
    bot.send_message(message.from_user.id, "Укажите удаленность от центра (диaпазон через пробел)!")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price'] = message.text


@bot.message_handler(state=UserInfoState.distance)
def get_distance(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.hotels_count, message.chat.id)
    bot.send_message(message.from_user.id, "Укажите количество отелей!")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['distance'] = message.text


@bot.message_handler(state=UserInfoState.hotels_count)
def get_hotels_count(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
    bot.send_message(message.from_user.id, 'Показывать фото?', reply_markup=send_photo())

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['hotels_count'] = message.text
        data['result'] = request_properties(data['dest_id'], data['check_in'],
                                            data['check_out'], data['hotels_count'])


@bot.callback_query_handler(func=None, state=UserInfoState.photo)
def get_photo(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id, text='Готово!')
    if call.data in ['yes', 'no']:
        if call.data == 'yes':
            bot.edit_message_text('Сколько фото показывать?', call.message.chat.id, call.message.message_id)

        elif call.data == 'no':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Нажмите "Дальше" для продолжения', reply_markup=farther())

        bot.set_state(call.message.chat.id, UserInfoState.photos_count, call.message.chat.id)
        with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
            data['photo'] = call.data

    else:
        bot.send_message(call.message.chat.id, 'Нет такого ответа!')


@bot.message_handler(state=UserInfoState.photos_count)
def send_result(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['photos_count'] = message.text

        for item in range(len(data['result'])):
            bot.send_message(message.from_user.id,
                             f'Загружаю инфу по отелю № {item + 1}...',
                             reply_markup=start_markup())
            if data['photos_count'].isdigit():
                show_photo = map(InputMediaPhoto, request_photo(message.text, data["result"][item]["id"]))
                bot.send_media_group(message.chat.id, show_photo)

            text = f'Название отеля: {data["result"][item]["name"]}\n' \
                   f'Адрес: {data["result"][item]["address"]}\n' \
                   f'Удалённость от центра: {data["result"][item]["distance"]}\n' \
                   f'Цена за ночь: {data["result"][item]["price"]}\n' \
                   f'Суммарная стоимость: ' \
                   f'${int(data["result"][item]["price"][1:]) * data["count_days"]}\n' \
                   f'Подробнее: {data["result"][item]["url"]}'

            bot.send_message(message.from_user.id, text)

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.from_user.id, 'Для продолжения нажмите любую кнопку...')
