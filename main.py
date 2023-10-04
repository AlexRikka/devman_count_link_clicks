import requests
import os
import argparse
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
    bitly_access_token = os.environ['BITLY_ACCESS_TOKEN']
    parser = argparse.ArgumentParser()
    parser.add_argument('link',
                        help='Ссылка для сокращения или подсчета кликов')
    user_input = parser.parse_args().link

    try:
        if is_bitlink(bitly_access_token, user_input):
            clicks_count = count_clicks(bitly_access_token, user_input)
            print('Количество переходов по короткой ссылке ', clicks_count)
        else:
            bitlink = shorten_link(bitly_access_token, user_input)
            print('Битлинк ', bitlink)
    except requests.exceptions.HTTPError:
        print("Вы ввели неправильную ссылку.")


if __name__ == '__main__':
    main()
