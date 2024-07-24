import requests
import csv
import time
from bs4 import BeautifulSoup


with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            'Имя', 'Кол-во слушателей', 'Последний релиз', 'Ссылка 1',
            'Ссылка 2', 'Ссылка 3', 'Ссылка 4', 'Ссылка 5', 'Ссылка 6'
        )
    )

print('Введите id артистов через пробел')

artists_id = input().split()

for artist_id in artists_id:
    artist_main_url = f'https://music.yandex.ru/artist/{artist_id}'
    artist_info_url = f'https://music.yandex.ru/artist/{artist_id}/info'

    artist_main_response = requests.session().get(artist_main_url)
    artist_main_response.encoding = 'UTF-8'
    time.sleep(100)
    artist_info_response = requests.session().get(artist_info_url)
    artist_info_response.encoding = 'UTF-8'
    time.sleep(100)

    bs_main = BeautifulSoup(artist_main_response.text, 'lxml')
    bs_info = BeautifulSoup(artist_info_response.text, 'lxml')


    name = bs_main.find(
        'h1', class_='page-artist__title typo-h1 typo-h1_big'
    ).text

    listeners = bs_main.find(
        'div', class_='page-artist__summary typo deco-typo-secondary'
    ).find(
        'span'
    ).text

    last_release = bs_main.find(
        'div', class_='album__year deco-typo-secondary typo-add'
    ).text

    links = bs_info.find_all(
        class_='d-link deco-link page-artist__link typo deco-pane_show-hover d-link_no-hover-color deco-link_no-hover-color'
    )

    link_data = []

    for link in links:
        link_url = link.get('href')
        link_data.append(link_url)

    data = [
        name, listeners, last_release,
    ]

    data.extend(link_data)

    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            data
        )