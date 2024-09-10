import requests
import os
from urllib.parse import urlparse

СССС = os.environ['CCCC']

API_URL_SHORTEN_WITH_APIVK = 'https://api.vk.com/method/utils.getShortLink'
API_URL_STATS_WITH_APIVK = 'https://api.vk.com/method/utils.getLinkStats'
API_VERSION = '5.131'


def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme in ['http', 'https'], parsed_url.netloc])


def is_shortened_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == 'vk.cc'


def shorten_link(access_token, long_url):
    if not is_valid_url(long_url):
        return None, "Ошибка: введен некорректный URL."

    params = {
        'access_token': access_token,
        'url': long_url,
        'v': API_VERSION
    }
    try:
        response = requests.get(API_URL_SHORTEN_WITH_APIVK, params=params)
        return handle_vk_response(response, is_shortening=True)
    except requests.exceptions.RequestException as e:
        return None, f"Ошибка при запросе: {e}"


def count_clicks(access_token, url_key):
    params = {
        'access_token': access_token,
        'key': url_key,
        'v': API_VERSION
    }
    try:
        response = requests.get(API_URL_STATS_WITH_APIVK, params=params)
        return handle_vk_response(response, is_shortening=False)
    except requests.exceptions.RequestException as e:
        return None, f"Ошибка при запросе: {e}"


def handle_vk_response(response, is_shortening):
    try:
        response.raise_for_status()
        result = response.json()
        if 'response' in result:
            if is_shortening:
                shortened_url = result['response']['short_url']
                url_key = result['response']['key']
                return shortened_url, url_key, None
            else:
                click_count = result['response'].get('clicks', 0)
                return click_count, None
        elif 'error' in result:
            error_code = result['error'].get('error_code')
            error_message = result['error'].get('error_msg')
            return None, f"Ошибка {error_code}: {error_message}"
        else:
            return None, "Неизвестная ошибка: ответ не содержит ожидаемых данных."
    except ValueError as e:
        return None, f"Ошибка при обработке JSON: {e}"
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP ошибка: {e}"


def print_result(shortened_url=None, url_key=None, click_count=None, error_message=None):
    if error_message:
        print(error_message)
    if shortened_url:
        print(f"Сокращенная ссылка: {shortened_url}")
    if click_count is not None:
        print(f"Количество кликов по ссылке: {click_count}")


def main():
    long_url_input = input("Введите ссылку: ")
    access_token = СССС
    if is_shortened_link(long_url_input):
        url_key = long_url_input.split('/')[-1]
        click_count, error_message = count_clicks(access_token, url_key)
        print_result(click_count=click_count, error_message=error_message)
    else:
        shortened_url, url_key, error_message = shorten_link(access_token, long_url_input)
        print_result(shortened_url=shortened_url, url_key=url_key, error_message=error_message)


if __name__ == '__main__':
    main()









