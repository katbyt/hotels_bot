import requests
from config_data.log_info import my_logger


def request_to_api(url, headers, querystring):
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        if response.status_code == requests.codes.ok:
            my_logger.info('Запрос к API прошел успешно. Возврат результата.')
            return response
    except requests.exceptions.ConnectTimeout:
        my_logger.warning('Время ожидания истекло. Нет ответа от API.')
        return 'Время вышло. Соединение не установлено.' \
               'Попробуйте повторить попытку позже.'
