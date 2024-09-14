
import requests
import os
from urllib.parse import urlparse

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
        raise ValueError("Некорректный URL.")

    params = {
        'access_token': access_token,
        'url': long_url,
        'v': API_VERSION
    }
    response = requests.get(API_URL_SHORTEN_WITH_APIVK, params=params)
    return handle_vk_response(response, is_shortening=True)


def count_clicks(access_token, url_key):
    params = {
        'access_token': access_token,
        'key': url_key,
        'v': API_VERSION
    }
    response = requests.get(API_URL_STATS_WITH_APIVK, params=params)
    return handle_vk_response(response, is_shortening=False)


def handle_vk_response(response, is_shortening):
    response.raise_for_status()
    result = response.json()
    if 'response' in result:
        if is_shortening:
            shortened_url = result['response']['short_url']
            url_key = result['response']['key']
            return shortened_url, url_key
        else:
            click_count = result['response'].get('clicks', 0)
            return click_count
    elif 'error' in result:
        error_code = result['error'].get('error_code')
        error_message = result['error'].get('error_msg')
        raise Exception(f"Ошибка {error_code}: {error_message}")
    else:
        raise Exception("Неизвестная ошибка: ответ не содержит ожидаемых данных.")


def main():
    long_url_input = input("Введите ссылку: ")
    if not is_valid_url(long_url_input):
        print("Ошибка: введен некорректный адрес.")
        return
<<<<<<< Updated upstream
    VK_TOKEN_API = os.environ.get('CCCC')
    if VK_TOKEN_API is None:
=======
    vk_api_short_link_token = os.environ.get('CCCC')
    if vk_api_short_link_token is None:
>>>>>>> Stashed changes
        print("Ошибка: переменная окружения 'CCCC' не установлена.")
        return

    try:
        if is_shortened_link(long_url_input):
            url_key = long_url_input.split('/')[-1]
<<<<<<< Updated upstream
            click_count = count_clicks(VK_TOKEN_API, url_key)
            print(f"Количество кликов по сокращенной ссылке: {click_count}")
        else:
            shortened_url, url_key = shorten_link(VK_TOKEN_API, long_url_input)
=======
            click_count = count_clicks(vk_api_short_link_token, url_key)
            print(f"Количество кликов по сокращенной ссылке: {click_count}")
        else:
            shortened_url, url_key = shorten_link(vk_api_short_link_token, long_url_input)
>>>>>>> Stashed changes
            print(f"Сокращенная ссылка: {shortened_url}")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
    except Exception as e:
        if "100" in str(e):
            print("Ошибка: неправильно введена ссылка.")
        else:
            print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    main()












