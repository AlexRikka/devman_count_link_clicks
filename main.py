import requests
import os
from dotenv import load_dotenv


def is_bitlink(bitly_access_token, link):
    headers = {'Authorization': bitly_access_token}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    response = requests.get(url, headers=headers)
    return response.ok


def count_clicks(bitly_access_token, bitlink):
    headers = {'Authorization': bitly_access_token}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def shorten_link(bitly_access_token, link):
    headers = {'Authorization': bitly_access_token}
    body = {'long_url': link}
    url = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def main():
    load_dotenv()
    BITLY_ACCESS_TOKEN = os.getenv("BITLY_ACCESS_TOKEN")
    user_input = input("Введите ссылку: ")
    bitlink = user_input
    if is_bitlink(BITLY_ACCESS_TOKEN, user_input):
        try:
            clicks_count = count_clicks(BITLY_ACCESS_TOKEN, bitlink)
            print('Количество переходов по короткой ссылке ', clicks_count)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    else:
        try:
            bitlink = shorten_link(BITLY_ACCESS_TOKEN, user_input)
            print('Битлинк ', bitlink)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


if __name__ == '__main__':
    main()
