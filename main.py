import requests
from fake_headers import Headers
from pprint import pprint
from bs4 import BeautifulSoup
from time import sleep
import json

Django = 'Django'
Flask = 'Flask'
list_vacancy = []

def get_headers():
    return Headers(browser="chrome", os="win").generate()

for page in range(0,10):
    sleep(0.5)
    html_data = requests.get(f'https://spb.hh.ru/search/vacancy?text=Python&salary=&area=1&area=2&ored_clusters=true&enable_snippets=true&page={page}',headers=get_headers()).text
    soup = BeautifulSoup(html_data, "lxml")
    tag_all_vacancy = soup.find('div', id="a11y-main-content")
    vacanceses = tag_all_vacancy.find_all('div', class_='vacancy-serp-item__layout')
    # pprint(tag_all_vacancy)
    for vacancy in vacanceses:
        info = vacancy.find('div', class_='g-user-content').find_all('div', class_='bloko-text')
        desc = []
        for i in info:
            desc.append(i.text)
        dict_vacancy = {}
        for text in desc:
            if Django in text and Flask in text:
                tag_a = vacancy.find_all('a')[0]
                title = tag_a.text
                url = tag_a['href']
                try:
                    salary = vacancy.find('span', class_='bloko-header-section-3').text.replace('\u202f', ' ')
                except:
                    salary = None
                company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
                city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
                dict_vacancy['title'] = title
                dict_vacancy['url'] = url
                dict_vacancy['salary'] = salary
                dict_vacancy['company'] = company
                dict_vacancy['city'] = city
                list_vacancy.append(dict_vacancy)
# pprint(list_vacancy)

with open('JOB.json', "w", encoding='UTF-8') as f:
    json.dump(list_vacancy, f, ensure_ascii=False, indent=2)





