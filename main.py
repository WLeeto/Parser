from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'}

URL = 'https://tproger.ru/'

response = requests.get(URL, headers=HEADERS)
text = response.text
soup = bs(text, features="html.parser")

to_check = {
    'date': [],
    'header': [],
    'href': [],
    'discription': []
}

result = []


def get_headers():
    # достаем заголовки
    header = soup.find_all(class_="article__title article__title--icon")
    for head in header:
        h = head.find("a").text
        new = h.replace('\n', '')
        to_check["header"].append(new)


def get_discription():
    # достаем описания
    discription = soup.find_all(class_="article__excerpt article__excerpt--icon")
    for d in discription:
        new = d.text.replace('\n', '')
        to_check["discription"].append(new)


def get_hrefs():
    # достаем ссылки
    all_href = soup.find_all(class_="article__title article__title--icon")
    for h in all_href:
        href = h.find("a").get("href")
        to_check["href"].append(href)


def get_dates():
    # достаем даты
    for h in to_check['href']:
        NEW_URL = h

        response = requests.get(NEW_URL, headers=HEADERS)
        text = response.text
        soup = bs(text, features="html.parser")

        dates = soup.find(class_="header-meta__statistics").find("time").get("datetime")
        to_check["date"].append(dates)


def find_words(list):
    for word in list:
        for i in range(0, len(to_check["discription"])):
            if word in to_check["discription"][i] or word in to_check["header"][i]:
                result.append([to_check["date"][i], to_check["header"][i], to_check["href"][i]])


if __name__ == "__main__":
    get_discription()
    get_hrefs()
    get_dates()
    get_headers()
    # pprint(to_check)
    keywords = ['дизайн', 'фото', 'web', 'python', 'написать']
    find_words(keywords)

    print(f'Поиск по ключевым словам {keywords}'
          f'Найдены следующие совпадения:\n')

    for i in result:
        print(f'Дата: {i[0]}\n'
              f'Заголовок: {i[1]}\n'
              f'Описание: {i[2]}\n')

