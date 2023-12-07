from bs4 import BeautifulSoup
import requests


### Парсим интересующий нас гороскоп с гороскопов mail.ru
def horoscope(mark):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
    }

    url = f'https://horo.mail.ru/prediction/{mark}/today/'
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    all_horo_text = soup.find(class_="article__item article__item_alignment_left article__item_html")
    horo = str(all_horo_text)[75:].replace('<p>', '').replace('</p>', '').replace('</div>', '')
    return horo
