import requests


def request_to_api(url, headers, querystring):
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
    except Exception:
        return 'Что-то пошло не так...'
