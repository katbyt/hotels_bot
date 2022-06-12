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
from rapi_api.request_photo import request_photo
from rapi_api.request_properties import request_properties
from database.hotels_db import User

ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def user_query(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_command'] = message.text

    bot.send_message(message.from_user.id, 'Введите город для поиска!')


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.set_state(message.from_user.id, UserInfoState.dest_id, message.chat.id)
        markup = city_markup(message.text)

        if isinstance(markup, str):
            bot.send_message(message.from_user.id, 'Что-то пошло не так...\nПовторите попытку позже!..')
        else:
            bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=markup)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Укажите, пжлст, корректное название города!')


@bot.callback_query_handler(func=None, state=UserInfoState.dest_id)
def get_check_in(call: CallbackQuery) -> None:
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
                                          locale="ru")

            bot.send_message(call.from_user.id,
                             f"Выберите {ALL_STEPS[step]}",
                             reply_markup=calendar)

            bot.set_state(call.from_user.id, UserInfoState.check_out, call.message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def handle_departure_date(call: CallbackQuery):
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

            if data['user_command'] in ['/lowprice', '/highprice']:
                bot.set_state(call.from_user.id, UserInfoState.hotels_count, call.message.chat.id)
                bot.send_message(call.message.chat.id, "Укажите количество отелей! (не более 5)")

            elif data['user_command'] == '/bestdeal':
                bot.set_state(call.from_user.id, UserInfoState.price, call.message.chat.id)
                bot.send_message(call.message.chat.id, "Укажите диaпазон цен в USD (через пробел)!")


@bot.message_handler(state=UserInfoState.hotels_count)
def get_hotels_count(message: Message) -> None:
    if message.text.isdigit() and (int(message.text) in range(1, 6)):
        bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
        bot.send_message(message.from_user.id, 'Показывать фото?', reply_markup=send_photo())

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_count'] = message.text

            price_min, price_max = 1, 10000
            distance = [0, 10000]

            if data['user_command'] == '/lowprice':
                sort_order = 'PRICE'
            elif data['user_command'] == '/highprice':
                sort_order = 'PRICE_HIGHEST_FIRST'
            elif data['user_command'] == '/bestdeal':
                sort_order = 'DISTANCE_FROM_LANDMARK'
                price_min, price_max = data['price']
                distance = data['distance']

            data['result'] = request_properties(data['dest_id'], data['check_in'],
                                                data['check_out'], data['hotels_count'],
                                                price_min, price_max, distance, sort_order)

            if isinstance(data['result'], str):
                bot.send_message(message.from_user.id, 'Что-то пошло не так...\nПовторите попытку позже!..')

    else:
        bot.send_message(message.from_user.id, 'Укажите, пжлст, корректное значение!')


@bot.callback_query_handler(func=None, state=UserInfoState.photo)
def get_photo(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id, text='Готово!')
    if call.data in ['yes', 'no']:
        if call.data == 'yes':
            bot.edit_message_text('Сколько фото показывать? (не более 5)',
                                  call.message.chat.id,
                                  call.message.message_id)

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
    if message.text.isdigit() and (int(message.text) in range(1, 6)):
        photos_count = int(message.text)
    else:
        photos_count = 0

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['photos_count'] = photos_count

        if data.get('result') is None:
            bot.send_message(message.from_user.id, 'Что-то пошло не так...\n'
                                                   'Попробуйте повторить попытку позже!..')
        else:
            for item in data['result']:
                number = data['result'].index(item)
                bot.send_message(message.from_user.id,
                                 f'Загружаю инфу по отелю № {number + 1}...',
                                 reply_markup=start_markup())
                if data['photos_count'] > 0:
                    photo_lst = request_photo(message.text, data["result"][number]["id"])
                    if isinstance(photo_lst, list):
                        show_photo = map(InputMediaPhoto, photo_lst)
                        bot.send_media_group(message.chat.id, show_photo)
                    else:
                        bot.send_message(message.from_user.id, 'Что-то сломалось... Фоточек не будет((')

                text = f'Название отеля: {data["result"][number]["name"]}\n' \
                       f'Адрес: {data["result"][number]["address"]}\n' \
                       f'Удалённость от центра: {data["result"][number]["distance"]}\n' \
                       f'Цена за ночь: {data["result"][number]["price"]}\n' \
                       f'Суммарная стоимость: ' \
                       f'${float(data["result"][number]["price"][1:].replace(",", ".")) * data["count_days"]}\n' \
                       f'Подробнее: {data["result"][number]["url"]}'

                User.create(user_id=message.from_user.id, command=data['user_command'], history=text)

                bot.send_message(message.from_user.id, text, disable_web_page_preview=True)

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.from_user.id, 'Для продолжения выберите новую команду...')
