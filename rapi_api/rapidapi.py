import requests


def request_to_api(url, headers, querystring):
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        if response.status_code == requests.codes.ok:
            return response
    except requests.exceptions.ConnectTimeout:
        return 'Время вышло. Соединение не установлено.' \
               'Попробуйте повторить попытку позже.'
