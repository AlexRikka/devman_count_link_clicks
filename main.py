import requests
import os
from dotenv import load_dotenv


def is_bitlink(token, link):
    Headers = {'Authorization': token}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    response = requests.get(url, headers=Headers)
    return response.ok


def count_clicks(token, bitlink):
    Headers = {'Authorization': token}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=Headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def shorten_link(token, link):
    Headers = {'Authorization': token}
    Body = {'long_url': link}
    url = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(url, json=Body, headers=Headers)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    user_input = input("Введите ссылку: ")
    bitlink = user_input
    if not is_bitlink(token, user_input):
        try:
            bitlink = shorten_link(token, user_input)
            print('Битлинк ', bitlink)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    else:
        try:
            clicks_count = count_clicks(token, bitlink)
            print('Количество переходов по короткой ссылке ', clicks_count)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

