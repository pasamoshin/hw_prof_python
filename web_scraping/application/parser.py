import json
import re
from bs4 import BeautifulSoup as bs
import requests
from fake_headers import Headers
from pprint import pprint


VACANCYS_LICT = []


class WebRequest():
    def __init__(self, url, browser, os):
        self.url = 'https://spb.hh.ru' + url
        self.headers = Headers(browser=browser, os=os).generate()

    def request(self):
        req = requests.get(self.url, headers=self.headers)

        if req.status_code == 200:
            return req.text
        else:
            print(req)


class Parsing():
    def __init__(self, data) -> None:
        self.soup = bs(data, features='lxml')

    def filling_values(self, list):
        if list == None:
            list = '-'
        else:
            list = list.text
        return list

    def get_link_next_page(self):
        try:
            link_next = self.soup.find('a', {'data-qa': 'pager-next'})['href']
        except:
            link_next = None
        return link_next

    def get_vacancies(self, currency=None, *filter):
        if filter == (): # Для удобства сравнения (ниже по коду), заполняею кортеж пустым значением
            filter = ([''],)




        data = self.soup.find(
            id='a11y-main-content').find_all(class_='vacancy-serp-item__layout') # Получение всего блока с вакансиями 

        num_vacancy = 1 # считчик вакансий (на одной страинце 20 вакансий)
        for vacancy in data:
            name = vacancy.find(class_='serp-item__title').text
            organization = vacancy.find(
                class_='bloko-link bloko-link_kind-tertiary').text

            compensation = vacancy.find(
                'span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            compensation = self.filling_values(compensation)
            
            # фильтр на валюту
            if currency == 'USD':
                if currency not in compensation:
                    continue
                

            city = vacancy.find(
                'div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]

            description = vacancy.find(
                'div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
            description = self.filling_values(description)

            requirements = vacancy.find(
                'div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
            requirements = self.filling_values(requirements)

            link = vacancy.find(class_='serp-item__title')['href']


            # если есть искомы слова, заполняем только те вакансии в которых есть указанные в фильтре слова
            if filter[0][0] != '':
                des_req = description + '---' + requirements  # Оъежиняю для разового поиска по двум значениям
                for i in filter[0]:
                    inverse_i = i[0].swapcase() # Получаем инверсию регистра первой буквы
                    filter_value = re.search(
                        f'[{i[0]}{inverse_i}]{i[1:]}', des_req)
                    if filter_value:
                        des_req = des_req.split('---')
                        description = des_req[0]
                        requirements = des_req[1]

                        vacancy = {'name': name, 'organization': organization,
                                   'compensation': compensation, 'city': city,
                                   'description': description, 'requirements': requirements,
                                   'link': link
                                   }
                        VACANCYS_LICT.append(vacancy)
            else:
                vacancy = {'name': name, 'organization': organization,
                           'compensation': compensation, 'city': city,
                           'description': description, 'requirements': requirements,
                           'link': link
                           }
                VACANCYS_LICT.append(vacancy)
            # print(vacancy)
            del vacancy
            print('-Обработано статей на странице: ', num_vacancy)
            num_vacancy += 1

def set_currency():
    while 1:
        currency = str(input('Зарплата в "$"? (да/нет)'))
        if (currency == '') or (currency == 'q'):
            break
        currency = currency.lower()[0]
        l = {
            'l':'USD', 'д':'USD',
            'y':'руб.', 'н':'руб.',
        }
        if currency in l:
            return l[currency]
        elif currency == 'q':
            break
        else:
            print('Введено неверное значение.')

def set_filter():
    filter = str(input('Введите через "/" слова по которым искать: '))
    filter = filter.replace(' ', '').split('/')

    return filter



def save_vacancies(data):
    ''' Функция сохранения вакансий в json.'''
    with open('vacancys.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print('парсик')
    
